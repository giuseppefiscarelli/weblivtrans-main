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

path_prot_db = os.path.join(os.path.dirname(lt_res.__file__),
                            'db', 'protocols_data.db')

HISTORY_DB_FILE = 'history.db'

# ---------------------------
# Helpers for per-session run
# ---------------------------

def get_run_id():
    """Return a stable unique ID for this browser session/run.

    Generated once and stored in the Flask session.
    Format: YYYYMMDD-HHMMSS_rand3digits (e.g., 20251103-104512_037)
    """
    rid = session.get("run_id")
    if not rid:
        ts = datetime.now().strftime("%Y%m%d-%H%M%S")
        rid = f"{ts}_{secrets.randbelow(1000):03d}"
        session["run_id"] = rid
    return rid


def get_tmp_db_file():
    """Temp DB file that is unique per session/run."""
    return f"tmp_{get_run_id()}.db"


def get_user_tag():
    """Human-friendly tag you can store in history.db."""
    return f"user_{get_run_id()}"


# ---------------------------
# History DB initialization
# ---------------------------

def init_history_db():
    """Initialize or migrate the history.db database."""
    conn = sqlite3.connect(HISTORY_DB_FILE)
    c = conn.cursor()

    # If the table doesn't exist, create with run_id and created_at
    columns_definition = ", ".join([f"{name} TEXT" for name in field_to_id])
    c.execute(
        f"""
        CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            run_id TEXT,
            created_at TEXT,
            {columns_definition}
        )
        """
    )

    # If table exists but lacks run_id/created_at, add them
    c.execute("PRAGMA table_info(patients)")
    existing_cols = {row[1] for row in c.fetchall()}
    if "run_id" not in existing_cols:
        c.execute("ALTER TABLE patients ADD COLUMN run_id TEXT")
    if "created_at" not in existing_cols:
        c.execute("ALTER TABLE patients ADD COLUMN created_at TEXT")

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

    c.execute(
        "CREATE TABLE IF NOT EXISTS responses (position INTEGER PRIMARY KEY, value TEXT)"
    )

    for field, idx in field_to_id.items():
        value = responses.get(field)
        if value is not None:
            c.execute(
                "REPLACE INTO responses (position, value) VALUES (?, ?)",
                (idx, str(value)),
            )

    conn.commit()
    conn.close()


def load_responses(db_file=None):
    """Load responses from the per-session temp database and map them to field names."""
    db_path = db_file or get_tmp_db_file()
    if not os.path.exists(db_path):
        return {}

    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("SELECT position, value FROM responses")
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
    """Validate responses against protocols.

    Returns
    -------
    matched_protocols : list[tuple[str, list[str]]]
        List of (protocol_name, warnings) for matched protocols.
    excluded_protocols : list[dict]
        One dict per excluded protocol with keys:
          - protocol_idx (int)
          - protocol_name (str)
          - warnings (list[str])
          - failed (list[dict]) where each dict has keys:
              - condition_index (int)  # query_index (0-based)
              - condition_key (str)
              - requirements (list[str|None])
                  protocol cell(s) for each field involved in the condition,
                  aligned with 'fields'/'values'.
              - fields (list[str])
              - values (list)          # coerced (numeric->float), may include None
    total_protocols : int
        Total number of protocols evaluated.
    """

    def evaluate_condition(condition_func, values):
        """Evaluate the condition with the standard missing-data policy.

        - If all values are None -> treat as satisfied (True).
        - If some values are None -> replace those with Dummy().
        """
        if values is None or all(v is None for v in values):
            return True
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

    protocols_warns = {}
    for row in warns_rows:
        protocol_name = row[1]
        warnings = list(filter(None, row[2:]))
        protocols_warns[protocol_name] = warnings

    protocols_rows = protocols_rows[1:]  # Skip header row in protocols_dataset

    # Process protocols data
    protocols_list, conditions_list = [], []
    for row in protocols_rows:
        protocols_list.append(row[0])
        conditions_list.append(row[1:])

    matched_protocols = []
    excluded_protocols = []
    total_protocols = len(conditions_list)

    for prot_idx, protocol_conditions in enumerate(conditions_list):
        protocol_name = protocols_list[prot_idx]
        warnings = protocols_warns.get(protocol_name, [])

        # Step 1: build one condition_key per query_index.
        condition_keys = []
        for col_indices in query_to_field:
            parts = []
            for col_idx in col_indices:
                cell = None
                try:
                    cell = protocol_conditions[col_idx]
                except Exception:
                    cell = None
                if cell is not None and cell != '':
                    parts.append(cell)
            condition_keys.append(''.join(parts))

        # Step 2: evaluate all query conditions (NO break) and record ALL failures.
        failed_conditions = []

        for query_index, condition_key in enumerate(condition_keys):
            if not condition_key:
                continue
            if query_index >= len(query_data):
                continue

            query_dict = query_data[query_index]
            condition_func = query_dict.get(condition_key)

            field_indices = query_to_field[query_index]
            field_names = [fields_data[idx].name for idx in field_indices]
            values = [responses.get(fname) for fname in field_names]

            # Per-field inclusion parameter(s): raw protocol cell for each field in this query.
            requirements = []
            for idx in field_indices:
                try:
                    requirements.append(protocol_conditions[idx])
                except Exception:
                    requirements.append(None)

            # Coerce numeric/decimal inputs
            for k, field_idx in enumerate(field_indices):
                field_info = fields_data[field_idx]
                v = values[k]
                if field_info.type in ['numeric', 'decimal']:
                    if v is not None and v != '':
                        try:
                            values[k] = float(v)
                        except ValueError:
                            values[k] = None
                    else:
                        values[k] = None

            # Evaluate
            result = True
            if condition_func is None:
                result = False
            else:
                try:
                    result = evaluate_condition(condition_func, values)

                    # --- Override logic for Histology N and T ---
                    if (not result) and ("unless >2 years from resection" in condition_key):
                        if responses.get('crc_resection_time') == ">24":
                            result = True
                except Exception:
                    result = False

            if not result:
                failed_conditions.append({
                    "condition_index": int(query_index),
                    "condition_key": str(condition_key),
                    "requirements": list(requirements),
                    "fields": list(field_names),
                    "values": list(values),
                })

        if not failed_conditions:
            matched_protocols.append((protocol_name, warnings))
        else:
            excluded_protocols.append({
                "protocol_idx": int(prot_idx),
                "protocol_name": str(protocol_name),
                "warnings": list(warnings),
                "failed": failed_conditions,
            })

    return matched_protocols, excluded_protocols, total_protocols


@app.route("/export_patient_info", methods=["POST"])
def export_patient_info():
    """Generate patient report and display it in a new HTML page."""
    init_history_db()

    # Load responses from the per-session temp DB
    responses = load_responses()

    # Insert into history.db
    conn = sqlite3.connect(HISTORY_DB_FILE)
    c = conn.cursor()

    patient_data = [responses.get(field_info.name, "") for field_info in fields_data]
    field_names = [field_info.name for field_info in fields_data]

    run_id = get_user_tag()  # e.g., 'user_20251103-104512_037'
    created_at = datetime.now().isoformat(timespec="seconds")

    insert_cols = ["run_id", "created_at"] + field_names
    placeholders = ",".join(["?"] * len(insert_cols))
    insert_vals = [run_id, created_at] + patient_data

    c.execute(
        f"INSERT INTO patients ({','.join(insert_cols)}) VALUES ({placeholders})",
        insert_vals,
    )

    conn.commit()
    conn.close()

    matched_protocols, _, total_protocols = validate_responses(responses)
    session["matched_protocols"] = matched_protocols
    session["total_protocols"] = int(total_protocols)

    success_message = f"Matched protocols: {len(matched_protocols)}/{total_protocols}"
    if not matched_protocols:
        matched_protocols = [("No protocols are adoptable for the patient.", [])]

    return render_template(
        "patient_report.html",
        responses=responses,
        matched_protocols=matched_protocols,
        fields_data=fields_data,
        success_message=success_message,
    )


# Route handling for each section
@app.route('/')
def index():
    return redirect(url_for('home'))


@app.route("/home")
def home():
    # Ensure a run_id exists early, so tmp file name is fixed for this session
    _ = get_run_id()
    return render_template("home.html")


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

    responses = load_responses()
    return render_template('section4.html', responses=responses)


@app.route("/section5", methods=["GET", "POST"])
def section5():
    if request.method == "POST":
        form_data = request.form.to_dict()
        disease_trend = form_data.get("disease_trend")
        if disease_trend != "partial_response":
            form_data["partial_response"] = None

        save_responses(form_data)

        # Load all responses and validate
        responses = load_responses()
        matched_protocols, _, total_protocols = validate_responses(responses)

        # Store session summary
        session["total_protocols"] = int(total_protocols)
        if not matched_protocols:
            session["matched_protocols"] = [("No protocols are adoptable for the patient.", [])]
        else:
            session["matched_protocols"] = matched_protocols

        return redirect(url_for("results_page"))

    responses = load_responses()
    return render_template("section5.html", responses=responses)


@app.route("/results_page")
def results_page():
    matched_protocols = session.get("matched_protocols", [])
    total_protocols = session.get("total_protocols")

    # Fallback: compute if user landed here without going through section5
    if total_protocols is None:
        responses = load_responses()
        mp, _, tp = validate_responses(responses)
        total_protocols = int(tp)
        session["total_protocols"] = total_protocols
        matched_protocols = mp
        session["matched_protocols"] = mp

    n_matched = 0
    if matched_protocols:
        # If we stored sentinel, count as 0
        if (
            isinstance(matched_protocols, list)
            and len(matched_protocols) == 1
            and isinstance(matched_protocols[0], (list, tuple))
            and matched_protocols[0][0] == "No protocols are adoptable for the patient."
        ):
            n_matched = 0
        else:
            n_matched = len(matched_protocols)

    success_message = f"Matched protocols: {n_matched}/{total_protocols}"

    if n_matched == 0:
        matched_protocols = [("No protocols are adoptable for the patient.", [])]

    return render_template(
        "results_page.html",
        matched_protocols=matched_protocols,
        success_message=success_message,
        total_protocols=total_protocols,
    )


@app.route("/patient_report")
def patient_report():
    responses = load_responses()

    matched_protocols = session.get("matched_protocols", [])
    total_protocols = session.get("total_protocols")

    if total_protocols is None:
        mp, _, tp = validate_responses(responses)
        total_protocols = int(tp)
        matched_protocols = mp
        session["total_protocols"] = total_protocols
        session["matched_protocols"] = matched_protocols

    n_matched = 0
    if matched_protocols:
        if (
            isinstance(matched_protocols, list)
            and len(matched_protocols) == 1
            and isinstance(matched_protocols[0], (list, tuple))
            and matched_protocols[0][0] == "No protocols are adoptable for the patient."
        ):
            n_matched = 0
        else:
            n_matched = len(matched_protocols)

    success_message = f"Matched protocols: {n_matched}/{total_protocols}"

    if n_matched == 0:
        matched_protocols = [("No protocols are adoptable for the patient.", [])]

    return render_template(
        "patient_report.html",
        responses=responses,
        matched_protocols=matched_protocols,
        fields_data=fields_data,
        success_message=success_message,
    )


# Route to handle restart and delete current per-session tmp DB
@app.route("/restart")
def restart():
    """Restart by deleting this session's tmp DB and clearing the session."""
    try:
        if "run_id" in session:
            db_path = get_tmp_db_file()
            if os.path.exists(db_path):
                os.remove(db_path)
    finally:
        session.clear()

    return redirect(url_for("home"))


@app.route("/excluded_protocols")
def excluded_protocols():
    responses = load_responses()
    matched_protocols, excluded_protocols_list, total_protocols = validate_responses(responses)

    matched_message = (
        f"Matched protocols: {len(matched_protocols)}/{total_protocols}"
        if total_protocols
        else "Matched protocols: 0/0"
    )
    excluded_message = (
        f"Excluded protocols: {len(excluded_protocols_list)}/{total_protocols}"
        if total_protocols
        else "Excluded protocols: 0/0"
    )

    field_labels = {f.name: getattr(f, "label", f.name) for f in fields_data}

    return render_template(
        "excluded_protocols.html",
        excluded_protocols=excluded_protocols_list,
        total_protocols=total_protocols,
        matched_message=matched_message,
        excluded_message=excluded_message,
        field_labels=field_labels,
    )


if __name__ == "__main__":
    app.run(debug=True)
