import os
import secrets
import sqlite3
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, session

from lt_clear.fields_params import fields_data, query_data, query_to_field, \
    field_to_id, Dummy
import lt_clear.resources as lt_res

app = Flask(__name__, template_folder="resources/pages/templates",
            static_folder="resources/pages/static")
app.secret_key = secrets.token_hex(16)  # Secure secret key for session management

# ---- Paths to permanent protocols DB and history DB ----
path_prot_db = os.path.join(os.path.dirname(lt_res.__file__),
                            'db', 'protocols_data.db')
HISTORY_DB_FILE = 'history.db'

# ---------------------------
# Helpers for per-session run
# ---------------------------


def get_run_id():
    """
    Return a stable unique ID for this browser session/run.
    Generated once and stored in the Flask session.
    Format: YYYYMMDD-HHMMSS_rand3digits (e.g., 20251103-104512_037)
    """
    rid = session.get('run_id')
    if not rid:
        ts = datetime.now().strftime("%Y%m%d-%H%M%S")
        rid = f"{ts}_{secrets.randbelow(1000):03d}"
        session['run_id'] = rid
    return rid

def get_tmp_db_file():
    """Temp DB file that is unique per session/run."""
    return f"tmp_{get_run_id()}.db"

def get_user_tag():
    """
    A human-friendly tag you can also store in history.db.
    If you prefer 'user_' prefix instead of 'tmp_', use that here.
    """
    return f"user_{get_run_id()}"

# ---------------------------
# History DB initialization
# ---------------------------
def init_history_db():
    """Initialize or migrate the history.db database."""
    conn = sqlite3.connect(HISTORY_DB_FILE)
    c = conn.cursor()

    # If the table doesn't exist, create with run_id and created_at
    columns_definition = ', '.join([f"{name} TEXT" for name in field_to_id])
    c.execute(f'''
        CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            run_id TEXT,
            created_at TEXT,
            {columns_definition}
        )
    ''')

    # If table exists but lacks run_id/created_at, add them
    c.execute("PRAGMA table_info(patients)")
    existing_cols = {row[1] for row in c.fetchall()}
    if 'run_id' not in existing_cols:
        c.execute('ALTER TABLE patients ADD COLUMN run_id TEXT')
    if 'created_at' not in existing_cols:
        c.execute('ALTER TABLE patients ADD COLUMN created_at TEXT')

    conn.commit()
    conn.close()

# ---------------------------
# Temp responses (per session)
# ---------------------------
def save_responses(responses, db_file=None):
    """Save responses to the per-session temp database using positions as keys."""
    db_path = db_file or get_tmp_db_file()
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    # Create table if not exists with position as PRIMARY KEY
    c.execute('CREATE TABLE IF NOT EXISTS responses (position INTEGER PRIMARY KEY, value TEXT)')
    for field, idx in field_to_id.items():
        value = responses.get(field)
        if value is not None:
            c.execute('REPLACE INTO responses (position, value) VALUES (?, ?)', (idx, str(value)))
    conn.commit()
    conn.close()

def load_responses(db_file=None):
    """Load responses from the per-session temp database and map them to field names."""
    db_path = db_file or get_tmp_db_file()
    if not os.path.exists(db_path):
        return {}
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('SELECT position, value FROM responses')
    rows = c.fetchall()
    conn.close()
    responses = {}
    for position, value in rows:
        field_name = fields_data[position].name
        responses[field_name] = value
    return responses

# ---------------------------
# Protocol validation
# ---------------------------
def validate_responses(responses):
    """Validate responses against protocols."""
    def evaluate_condition(condition_func, values):
        """
        Evaluates the condition using the condition_func function and the list of values.
        - If all values are None, it returns True.
        - If only some values are None, it replaces them with Dummy.
        """
        # Case 1: all None
        if values is None or all(v is None for v in values):
            return True
        # Case 2: replace missing with Dummy
        new_values = [v if v is not None else Dummy() for v in values]
        return condition_func(*new_values)

    # Load protocols data from 'protocols_data.db'
    conn = sqlite3.connect(path_prot_db)
    c = conn.cursor()
    c.execute('SELECT * FROM protocols_dataset')
    protocols_rows = c.fetchall()
    c.execute('SELECT * FROM protocols_warns')
    warns_rows = c.fetchall()
    conn.close()

    # Map protocol names to warnings (list of strings)
    protocols_warns = {}
    for row in warns_rows:
        protocol_name = row[1]  # Protocol name is in the second column
        warnings = list(filter(None, row[2:]))  # Collect non-None warnings
        protocols_warns[protocol_name] = warnings

    # Skip header row in protocols_dataset
    protocols_rows = protocols_rows[1:]

    # Process protocols data
    protocols_list = []
    conditions_list = []
    for row in protocols_rows:
        protocol_name = row[0]
        conditions = row[1:]
        protocols_list.append(protocol_name)
        conditions_list.append(conditions)

    matched_protocols = []

    for i, protocol_conditions in enumerate(conditions_list):
        protocol_name = protocols_list[i]
        protocol_matched = True

        # Step 1: Build conditions
        conditions = []
        for q2f in query_to_field:
            condition = "".join(protocol_conditions[i] if protocol_conditions[i] is not None else "" for i in q2f)
            conditions.append(condition)

        # Step 2: Check conditions
        for query_index, condition_key in enumerate(conditions):
            if not condition_key:
                continue
            # Get the query dictionary
            try:
                query_dict = query_data[query_index]
            except IndexError:
                continue
            # Get the condition function
            condition_func = query_dict.get(condition_key)
            # Get the field indices for this query
            field_indices = query_to_field[query_index]
            # Get the field names
            field_names = [fields_data[idx].name for idx in field_indices]
            # Get the values from responses
            values = [responses.get(field_name) for field_name in field_names]
            # Convert values to appropriate types
            for idx, field_idx in enumerate(field_indices):
                field_info = fields_data[field_idx]
                value = values[idx]
                if field_info.type in ['numeric', 'decimal']:
                    if value is not None and value != '':
                        try:
                            values[idx] = float(value)
                        except ValueError:
                            values[idx] = None
                    else:
                        values[idx] = None
            # Evaluate
            try:
                result = evaluate_condition(condition_func, values)
                # Override logic for Histology N and T (custom case)
                if not result:
                    if "unless >2 years from resection" in condition_key:
                        if responses.get('crc_resection_time') is not None and responses.get('crc_resection_time') == ">24":
                            result = True
                if not result:
                    protocol_matched = False
                    break
            except Exception:
                protocol_matched = False
                break

        if protocol_matched:
            warnings = protocols_warns.get(protocol_name, [])
            matched_protocols.append((protocol_name, warnings))

    return matched_protocols

# ---------------------------
# Routes
# ---------------------------
@app.route('/export_patient_info', methods=['POST'])
def export_patient_info():
    """Generate patient report and display it in a new HTML page."""
    # Initialize history database if needed
    init_history_db()

    # Load responses from the per-session temp DB
    responses = load_responses()

    # Insert into history.db
    conn = sqlite3.connect(HISTORY_DB_FILE)
    c = conn.cursor()

    # Prepare data
    patient_data = [responses.get(field_info.name, '') for field_info in fields_data]
    field_names = [field_info.name for field_info in fields_data]

    # Prepend run_id and created_at
    run_id = get_user_tag()  # e.g., 'user_20251103-104512_037'
    created_at = datetime.now().isoformat(timespec='seconds')

    insert_cols = ['run_id', 'created_at'] + field_names
    placeholders = ','.join(['?'] * len(insert_cols))
    insert_vals = [run_id, created_at] + patient_data

    c.execute(f'''
        INSERT INTO patients ({','.join(insert_cols)}) VALUES ({placeholders})
    ''', insert_vals)

    conn.commit()
    conn.close()

    matched_protocols = validate_responses(responses)

    # Generate the report and render it in a new HTML page
    return render_template('patient_report.html', responses=responses, matched_protocols=matched_protocols,
                           fields_data=fields_data,
                           success_message=f"Matched protocols: {len(matched_protocols)}/27" if matched_protocols
                           else "No protocols are adoptable for the patient.")

@app.route('/')
def index():
    return redirect(url_for('home'))

@app.route('/home')
def home():
    # Ensure a run_id exists early, so tmp file name is fixed for this session
    _ = get_run_id()
    return render_template('home.html')

@app.route('/section1', methods=['GET', 'POST'])
def section1():
    if request.method == 'POST':
        form_data = request.form.to_dict()
        # Handle conditional fields
        other_malignancies = form_data.get('other_malignancies')
        if other_malignancies != 'yes':
            form_data['malignancies_timing'] = None
            form_data['malignancies_type'] = None
        save_responses(form_data)
        return redirect(url_for('section2'))
    else:
        responses = load_responses()
        return render_template('section1.html', responses=responses)

@app.route('/section2', methods=['GET', 'POST'])
def section2():
    if request.method == 'POST':
        form_data = request.form.to_dict()
        # Handle the conditional field 'resection_margin'
        location = form_data.get('location')
        if location != 'extraperitoneal_rectum':
            form_data['resection_margin'] = None
        save_responses(form_data)
        return redirect(url_for('section3'))
    else:
        responses = load_responses()
        show_resection_margin = responses.get('location') == 'extraperitoneal_rectum'
        return render_template('section2.html', responses=responses, show_resection_margin=show_resection_margin)

@app.route('/section3', methods=['GET', 'POST'])
def section3():
    if request.method == 'POST':
        form_data = request.form.to_dict()
        # Handle conditional fields
        prior_metastatic = form_data.get('prior_metastatic')
        if prior_metastatic != 'yes':
            form_data['metastatic_type'] = None
            form_data['timing_resection'] = None
        extrahepatic = form_data.get('extrahepatic')
        if extrahepatic != 'yes':
            form_data['extrahepatic_type'] = None
            form_data['resectable_lung_number'] = None
            form_data['resectable_lung_dimensions'] = None
        if form_data.get('extrahepatic_type') != 'resectable':
            form_data['resectable_lung_number'] = None
            form_data['resectable_lung_dimensions'] = None

        save_responses(form_data)
        return redirect(url_for('section4'))
    else:
        responses = load_responses()
        return render_template('section3.html', responses=responses)

@app.route('/section4', methods=['GET', 'POST'])
def section4():
    if request.method == 'POST':
        form_data = request.form.to_dict()
        systemic_therapy = form_data.get('systemic_therapy')
        if systemic_therapy != 'yes':
            form_data['chemotherapy_time'] = None
            form_data['chemotherapy_lines'] = None
        save_responses(form_data)
        return redirect(url_for('section5'))
    else:
        responses = load_responses()
        return render_template('section4.html', responses=responses)

@app.route('/section5', methods=['GET', 'POST'])
def section5():
    if request.method == 'POST':
        form_data = request.form.to_dict()
        disease_trend = form_data.get('disease_trend')
        if disease_trend != 'partial_response':
            form_data['partial_response'] = None
        save_responses(form_data)

        # Load all responses and validate
        responses = load_responses()
        matched_protocols = validate_responses(responses)
        if not matched_protocols:
            matched_protocols = [('No protocols are adoptable for the patient.', '')]
        session['matched_protocols'] = matched_protocols
        return redirect(url_for('results_page'))
    else:
        responses = load_responses()
        return render_template('section5.html', responses=responses)

@app.route('/results_page')
def results_page():
    matched_protocols = session.get('matched_protocols', [])
    if not matched_protocols:
        matched_protocols = [('No protocols are adoptable for the patient.', '')]
        success_message = "No protocols are adoptable for the patient."
    else:
        success_message = f"Matched protocols: {len(matched_protocols)}/27"
    return render_template('results_page.html',
                           matched_protocols=matched_protocols,
                           success_message=success_message)

@app.route('/patient_report')
def patient_report():
    responses = load_responses()
    matched_protocols = session.get('matched_protocols', [])
    if not matched_protocols:
        matched_protocols = [('No protocols are adoptable for the patient.', '')]
        success_message = "No protocols are adoptable for the patient."
    else:
        success_message = f"Matched protocols: {len(matched_protocols)}/27"
    return render_template('patient_report.html',
                           responses=responses,
                           matched_protocols=matched_protocols,
                           fields_data=fields_data,
                           success_message=success_message)

# Route to handle restart and delete current per-session tmp DB
@app.route('/restart')
def restart():
    """Restart by deleting this session's tmp DB and clearing the session."""
    # Delete this session's tmp file (if any)
    try:
        if 'run_id' in session:
            db_path = get_tmp_db_file()
            if os.path.exists(db_path):
                os.remove(db_path)
    finally:
        session.clear()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)

