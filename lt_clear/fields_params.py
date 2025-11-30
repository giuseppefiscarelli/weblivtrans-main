import collections

# Main fields data, as tuple of named tuples
# each tuple contains:
# . label
# . data type (field)
# . HTML section/page to which field belong
# . optionality
# . index in field of protocol DB for test
# . query parameters as dictionary

FieldInfo = collections.namedtuple(
    'FieldInfo', ('name', 'type', 'section', 'req', 'query_id')
)

fields_data = (
    # Section 1 Fields
    FieldInfo(  # 0: Age
        name='age',
        type='numeric',
        section=1,
        req=True,
        query_id=0
    ),
    FieldInfo(  # 1: ECOG
        name='ecog',
        type='radio-group',
        section=1,
        req=True,
        query_id=1,
        ),
        
    FieldInfo(  # 2: BMI
        name='bmi',
        type='radio-group',
        section=1,
        req=True,
        query_id=2,
    ),
    
    FieldInfo(  # 3: HBV
        name='hbv',
        type='radio-group',
        section=1,
        req=True,
        query_id=3,
    ),
    FieldInfo(  # 4: HCV
        name='hcv',
        type='radio-group',
        section=1,
        req=True,
        query_id=4,
    ),
    FieldInfo(  # 5: HIV
        name='hiv',
        type='radio-group',
        section=1,
        req=True,
        query_id=5,
    ),
    FieldInfo(  # 6: weight loss (last 6 month)
        name='weight_loss',
        type='radio-group',
        section=1,
        req=True,
        query_id=6,
    ),
    FieldInfo(  # 7: other malignancies
        name='other_malignancies',
        type='radio-group',
        section=1,
        req=True,
        query_id=7,
    ),
    FieldInfo(  # 8: malignancies timing 
        name='malignancies_timing',
        type='radio-group',
        section=1,
        req=True,
        query_id=8,
    ),
    FieldInfo(  # 9: malignancies_type   
        name='malignancies_type',    
        type='radio-group',
        section=1,
        req=True,
        query_id=8,
    ),
    FieldInfo(  # 10: hb
        name='hb',
        type='form-group',
        section=1,
        req=True,
        query_id=9,
    ),
    FieldInfo(  # 11: wbc
        name='wbc',
        type='form-group',
        section=1,
        req=True,
        query_id=10,
    ),
    FieldInfo(  # 12: neutrophils
        name='neutrophils',
        type='form-group',
        section=1,
        req=True,
        query_id=11,
    ),
    FieldInfo(  # 13: platelets
        name='platelets',
        type='form-group',
        section=1,
        req=True,
        query_id=12,
    ),
    FieldInfo(  # 14: bilirubin
        name='bilirubin',
        type='form-group',
        section=1,
        req=True,
        query_id=13,
    ),
    FieldInfo(  # 15: ast_alt
        name='ast_alt',
        type='form-group',
        section=1,
        req=True,
        query_id=14,
    ),
    FieldInfo(  # 16: albumin
        name='albumin',
        type='radio-group',
        section=1,
        req=True,
        query_id=15,
    ),
    FieldInfo(  # 17: creatinine
        name='creatinine',
        type='form-group',
        section=1,
        req=True,
        query_id=16,
    ),
    FieldInfo(  # 18: egfr
        name='egfr',
        type='radio-group',
        section=1,
        req=True,
        query_id=17,
    ),
    FieldInfo(  # 19: cea
        name='cea',
        type='numeric',
        section=1,
        req=True,
        query_id=18,
    ),
    FieldInfo(  # 20: cea_trend
        name='cea_trend',
        type='form-group',
        section=1,
        req=True,
        query_id=18,
    ),     
    # Section 2 Fields
    FieldInfo(  # 21: crc_diagnosis_time
        name='crc_diagnosis_time',
        type='form-group',
        section=2,
        req=True,
        query_id=19
    ),

    FieldInfo(  # 22: crc_resection_time
        name='crc_resection_time',
        type='form-group',
        section=2,
        req=True,
        query_id=20
    ),

    FieldInfo(  # 23: location
        name='location',
        type='form-group',
        section=2,
        req=True,
        query_id=21,
    ),
    FieldInfo(  # 24: resection_margin
        name='resection_margin',
        type='form-group',
        section=2,
        req=True,
        query_id=21,
    ),
    FieldInfo(  # 25: radical_resection
        name='radical_resection',
        type='radio-group',
        section=2,
        req=True,
        query_id=22,
    ),
    FieldInfo(  # 26: standard_treatment
        name='standard_treatment',
        type='radio-group',
        section=2,
        req=True,
        query_id=23,
    ),
    FieldInfo(  # 27: histology_t
        name='histology_t',
        type='radio-group',
        section=2,
        req=True,
        query_id=24,
    ),
    FieldInfo(  # 28: histology_n
        name='histology_n',
        type='radio-group',
        section=2,
        req=True,
        query_id=25,
    ),
    FieldInfo(  # 29: histology_r
        name='histology_r',
        type='radio-group',
        section=2,
        req=True,
        query_id=26,
    ),
    FieldInfo(  # 30: braf
        name='braf',
        type='radio-group',
        section=2,
        req=True,
        query_id=27,
    ),
    FieldInfo(  # 31: ras
        name='ras',
        type='radio-group',
        section=2,
        req=True,
        query_id=28,
    ),
    FieldInfo(  # 32: microsatellite
        name='microsatellite',
        type='radio-group',
        section=2,
        req=True,
        query_id=29,
    ),
    #section 3
    FieldInfo(  # 33: prior_metastatic
        name='prior_metastatic',
        type='radio-group',
        section=3,
        req=True,
        query_id=30,
    ),
    FieldInfo(  # 34: metastatic_type
        name='metastatic_type',
        type='radio-group',
        section=3,
        req=True,
        query_id=30,
    ),
    FieldInfo(  # 35: timing_resection
        name='timing_resection',
        type='form-group',
        section=3,
        req=True,
        query_id=30,
    ),
    FieldInfo(  # 36: local_recurrence
        name='local_recurrence',
        type='radio-group',
        section=3,
        req=True,
        query_id=31,
    ),
    FieldInfo(  # 37: num_hepatic_lesions_before_chemo
        name='num_hepatic_lesions_before_chemo',
        type='radio-group',
        section=3,
        req=True,
        query_id=32,
    ),
    FieldInfo(  # 38: dim_largest_lesion_before_chemo
        name='dim_largest_lesion_before_chemo',
        type='radio-group',
        section=3,
        req=True,
        query_id=33,
    ),
    FieldInfo(  # 39: dim_largest_lesion_current
        name='dim_largest_lesion_current',
        type='form-group',
        section=3,
        req=True,
        query_id=34,
    ),
    FieldInfo(  # 40: vascular_invasion
        name='vascular_invasion',
        type='radio-group',
        section=3,
        req=True,
        query_id=35,
    ),
    FieldInfo(  # 41: diaphragmatic_invasion
        name='diaphragmatic_invasion',
        type='radio-group',
        section=3,
        req=True,
        query_id=36,
    ),
    FieldInfo(  # 42: extrahepatic
        name='extrahepatic',
        type='radio-group',
        section=3,
        req=True,
        query_id=37,
    ),
    FieldInfo(  # 43: extrahepatic_type
        name='extrahepatic_type',
        type='radio-group',
        section=3,
        req=True,
        query_id=37,
    ),
    FieldInfo(  # 44: resectable_lung_number
        name='resectable_lung_number',
        type='numeric',
        section=3,
        req=True,
        query_id=37,
    ),
    FieldInfo(  # 45: resectable_lung_dimensions
        name='resectable_lung_dimensions',
        type='decimal',
        section=3,
        req=True,
        query_id=37,
    ),
    
    # Section 4 Fields
    FieldInfo(  # 46: systemic_therapy
        name='systemic_therapy',
        type='radio-group',
        section=4,
        req=True,
        query_id=38,
    ),
    FieldInfo(  # 47: chemotherapy_time
        name='chemotherapy_time',
        type='radio-group',
        section=4,
        req=True,
        query_id=38,
    ),
    FieldInfo(  # 48: chemotherapy_lines
        name='chemotherapy_lines',
        type='radio-group',
        section=4,
        req=True,
        query_id=38,
    ),
    
    # Section 5 Fields
    FieldInfo(  # 49: disease_trend
        name='disease_trend',
        type='radio-group',
        section=5,
        req=True,
        query_id=39,
    ),
    FieldInfo(  # 50: stability_time
        name='stability_time',
        type='radio-group',
        section=5,
        req=True,
        query_id=39,
    ),
    FieldInfo(  # 51: partial_response
        name='partial_response',
        type='radio-group',
        section=5,
        req=True,
        query_id=39,
    ),
    FieldInfo(  # 52: trans_arterial_treatment
        name='trans_arterial_treatment',
        type='radio-group',
        section=5,
        req=True,
        query_id=39,
    )
)

query_data = [
    # 0: Age
    { '>18' : lambda age: age > 18,
          '18-70' : lambda age: 18 <= age <= 70,
          '18-68' : lambda age: 18 <= age <= 68,
          '18-75' : lambda age: 18 <= age <= 75,
          '18-65' : lambda age: 18 <= age <= 65,
          '18-73' : lambda age: 18 <= age <= 73,
          '18-77' : lambda age: 18 <= age <= 77,
          '>19' : lambda age: age > 19,
        },
    # 1: ECOG
    {
        '<2': lambda x: x in ['0', '1'],
        '0': lambda x: x == '0',
        '<3': lambda x: x in ['0', '1', '2'],
    },
    # 2: BMI
    {
        '<30': lambda x: x == '<30',
    },
    # 3: HBV infection
    {
        'no': lambda x: x == "no"
    },
    # 4: HCV
    {
        'negative': lambda x: x == "negative"
    },
    # 5: HIV
    {
        'negative': lambda x: x == "negative"
    },
    # 6: weight loss
    {
        '<10%': lambda x: x == "<10%"
    },
    # 7: other malignancies
    {
        'no': lambda x: x == "no"
    },
    # 8: malignancies timing AND malignancies_type
    {
        'low-risk': lambda x, y: y == "low-risk",
        '>5 years': lambda x, y: x == ">5 years",
        '>5 years if high risk, <5 years if low risk'*2:
            lambda x, y: (x == ">5 years" and y == "high-risk") or (y == "low-risk")
    },
    # 9: hb
    {   '>7.5': lambda x: x in ['7.5-9', '9-10', '10-12', '>12'],
        '>10': lambda x: x in ['10-12', '>12'],
        '>9': lambda x: x in ['9-10', '10-12', '>12'],
        '>12': lambda x: x == '>12'
    },
    # 10: wbc 
    {
        '>2500': lambda x: x in ['2500-3000', '3000-4000', '>4000'],
        '>4000': lambda x: x == '>4000',
        '>3000': lambda x: x in ['3000-4000', '>4000'],
    },
    # 11: neutrophils  <1000 vs 1000-1500 vs 1500-2500 vs >2500
    {
        '>1000': lambda x: x in ['1000-1500', '1500-2500', '>2500'],
        '>1500': lambda x: x in ['1500-2500', '>2500'],
        '>2500': lambda x: x == '>2500'
    },
    # 12: platelets <30.000 vs 30.000-75.000 vs 75.000-80.000 vs 80-100.000 vs 100.000-150.000 vs >150.000
    {
        '>30000': lambda x: x in ['30.000-60.000','60.000-75.000','75.000-80.000','80.000-100.000','100.000-150.000', '>150.000'],
        '>80000': lambda x: x in ['80.000-100.000','100.000-150.000', '>150.000'],
        '>60000': lambda x: x in ['60.000-75.000','75.000-80.000','80.000-100.000','100.000-150.000', '>150.000'],
        '>75000': lambda x: x in ['75.000-80.000','80.000-100.000','100.000-150.000', '>150.000'],
        '>100000': lambda x: x in ['100.000-150.000', '>150.000'],
        '>150000': lambda x: x == '>150.000'
    },
    # 13: bilirubin
    {
        '<2 times the upper normal value': lambda x: x in ["normal", "<1.5", "1.5-2"],
        '<1.5 times the upper normal value': lambda x: x in ["normal", "<1.5"],
        '<5 times the upper normal value': lambda x: x in ["normal", "<1.5", "1.5-2", "2-5"],
        'normal': lambda x: x == "normal"
    },
    # 14: ast_alt
    {
        'normal': lambda x: x == 'normal',
        '<5 times upper normal value': lambda x: x in ["normal", "<1.5", "1.5-2", "2-5"]
    },
    # 15: albumin
    {
        'yes': lambda x: x == 'normal',
    },
    # 16: creatinine
    {
        '<1.25 times upper normal level': lambda x: x in ["normal", "<1.25"],
        'normal': lambda x: x == "normal"
    },
    # 17: eGFR
    {
        '>90': lambda x: x == ">90",
        '>50': lambda x: x in ["50-60", "60-90", ">90"],
        '>60': lambda x: x in ["60-90", ">90"],
    },
    # 18: cea AND cea_trend
    {
        '<100': lambda x, y: x < 100,
        '<200': lambda x, y: x < 200,
        '<80': lambda x, y: x < 80,
        '<50': lambda x, y: x < 50,
        '<80stable or decreasing' : lambda x, y: x < 80 and y in ['stable', 'decreasing>50%', 'decreasing<50%'],        '<80 or decreasing >50%'*2: lambda x, y: x < 80 or y == 'decreasing>50%',
        'stable or decreasing': lambda x, y: y in ['stable', 'decreasing>50%', 'decreasing<50%'],
        '<100'+'stable or decreasing': lambda x, y: x < 100 and y in ['stable', 'decreasing>50%', 'decreasing<50%']
        
    },
    # Section 2
    # 19
    # Time elapsed from CRC diagnosis (months)
    {
        '>24' : lambda x : x == '>24',
        '>12' : lambda x : x in ['12-24','>24'],
        '>3' : lambda x : x in ['3-12','12-24','>24'],
    },

    # 20
    # Time elapsed from primary CRC resection (months) <3 vs 3-6 vs 6-10 vs 10-12 vs >12
    {
        '>12' : lambda x : x in ['12-24','>24'],
        '>10' : lambda x : x in ['10-12','12-24','>24'],
        '>6' : lambda x : x in ['6-10','10-12','12-24','>24'],
        '>3' : lambda x : x in ['3-6','6-10','10-12','12-24','>24'],
    },

    # 21: location AND resection_margin <1 mm vs 1-2 vs 2-20 vs >20
    {
        'any except extraperitoneal rectum': lambda x,y: x != "extraperitoneal_rectum",
        'any except right colon': lambda x,y: x != "right_colon",
        '<2 mm': lambda x,y: (x != "extraperitoneal_rectum") or (x == "extraperitoneal_rectum" and y in ['2-20', '>20']),
        '<1 mm': lambda x,y: (x != "extraperitoneal_rectum") or (x == "extraperitoneal_rectum" and y in ['1-2', '2-20', '>20']),
        '<20 mm': lambda x,y: (x != "extraperitoneal_rectum") or (x == "extraperitoneal_rectum" and y == '>20'),
    },
    # 22: radical_resection
    {
        'yes': lambda x: x == "yes"
    },
    # 23: standard_treatment
    {
        'yes': lambda x: x == "yes"
    },
    # 24: histology_t
    {
        '<T4B': lambda x: x in ['1', '2', '3', '4a'],
        '<T4': lambda x: x in ['1', '2', '3'],
        '<T4 unless >2 years from resection': lambda x: x in ['1', '2', '3'],
    },
    # 25: histology_n
    {
        '<N1': lambda x: x in ['0'],
        '<N2 unless >2 years from resection': lambda x: x in ['0', '1a', '1b', '1c'],
        '<N2': lambda x: x in ['0', '1a', '1b', '1c']
    },
    # 26: histology_r
    {
        '<R1': lambda x: x == '0'
    },
    # 27: braf
    {
        'wild-type': lambda x: x == "wild_type"
    },
    # 28: ras
    {
        'wild-type': lambda x: x == "wild_type"
    },
    # 29: microsatellite
    {
        "stable": lambda x: x == "stable"
    },
    # Section 3
    # 30: prior_metastatic AND metastatic_type AND timing_resection
    {
        'no': lambda x, y, z: x == 'no',
        '>1 year ling/hiluum; >2 years others': lambda x, y, z: (
            x == 'no' or 
            (x == 'yes' and (
                (y == 'resected_liver_lesion' and z in ('1 year - 2 years', '>2 years')) or
                (y in ('other', 'resected_lung_lesion') and z == '>2 years')
            ))
        ),
        'resected lung lesions>3 months': lambda x, y, z: (
            x == 'no' or  
          (x == 'yes' and y == 'resected_lung_lesion' and z in ('3 months - 6 months', '6 months - 1 year', '1 year - 2 years', '>2 years')
        )
        ),
        'resected lung lesions>6 months': lambda x, y, z: (
            x == 'no' or  
          (x == 'yes' and y == 'resected_lung_lesion' and z in ('6 months - 1 year', '1 year - 2 years', '>2 years')
        ))
    },
    
    # 31: local_recurrence
    {
        'no': lambda x: x == 'no',
        'no or yes but resected >2 years': lambda x: x in ['no', 'yes_res_2_years']
    },
    # 32: num_hepatic_lesions_before_chemo
    {
        '<20 before chemo': lambda x: x == '<20'
    },
    # 33: dim_largest_lesion_before_chemo
    {
        '<10 cm': lambda x: x == '<10'
    },
    # 34: dim_largest_lesion_current
    {
        '<10 cm': lambda x: x in ['<5','5-5.5','5.5-10'],
        '<5 cm': lambda x: x == '<5',
        '<5.5 cm': lambda x: x in ['5-5.5','<5']
    },
    # 35: vascular_invasion
    {
        'no': lambda x: x == 'no'
    },
    # 36: diaphragmatic_invasion
    {
        'no': lambda x: x == 'no'
    },
    # 37: extrahepatic AND extrahepatic_type AND resectable_lung_number AND resectable_lung_dimensions
    {
        'no': lambda x, y, z, k: x == 'no',
        'resectable lung lesions': lambda x, y, z, k: y == 'resectable',
        'resectable lung lesions'+'<15 mm': lambda x, y, z, k: y == 'resectable' and k < 15,
        'resectable lung lesions'+'<4': lambda x, y, z, k: y == 'resectable' and z < 4,
        'resectable lung lesions'+'<4'+'<15 mm': lambda x, y, z, k: y == 'resectable' and z < 4 and k < 15
    },
    # Section 4
    # 38: systemic_therapy AND chemotherapy_time <6 weeks vs 6-8 vs 8-12 vs 12-26 vs 26-104 vs >104 
    # AND chemotherapy_lines 1 vs 2 vs 3 vs >3
    {
        'yes': lambda x, y, z: x == 'yes',
        'no': lambda x, y, z: x == 'no',
        'yes'+'>6 weeks': lambda x, y, z: x == 'yes' and y in ['6-8','8-12','12-26','26-104','>104'],
        'yes'+'>8 weeks': lambda x, y, z: x == 'yes' and y in ['8-12','12-26','26-104','>104'],
        'yes'+'>12 weeks': lambda x, y, z: x == 'yes' and y in ['12-26','26-104','>104'],
        'yes'+'>26 weeks': lambda x, y, z: x == 'yes' and y in ['26-104','>104'],
        'yes'+'>104 weeks': lambda x, y, z: x == 'yes' and y == '>104',
        'yes'+'1': lambda x, y, z: x == 'yes' and z == '1',
        'yes'+'>6 weeks'+'1': lambda x, y, z: x == 'yes' and y in ['6-8','8-12','12-26','26-104','>104'] and z == '1',
        'yes'+'>12 weeks'+'1': lambda x, y, z: x == 'yes' and y in ['12-26','26-104','>104'] and z == '1',
        'yes'+'>6 weeks'+'>1': lambda x, y, z: x == 'yes' and y in ['6-8','8-12','12-26','26-104','>104'] and z in ['2','3','>3'],
        'yes'+'<3': lambda x, y, z: x == 'yes' and z in ['1','2'],
        'yes'+'<4': lambda x, y, z: x == 'yes' and z in ['1','2','3'],
        'yes'+'>8 weeks'+'<2': lambda x, y, z: x == 'yes' and y in ['8-12','12-26','26-104','>104'] and z in ['1','2'],
    },
    # Section 5
    # 39: disease_trend AND stability_time AND partial_response AND Received trans-arterial treatment
    {
        # Stable or Partial Response
        'stability or partial response': lambda x, y, z, k: x in ['stable', 'partial_response'],

        # Partial Response with different percentages
        'partial response'+'>10% RECIST OR >20% after trans-arterial treatment;'*2: lambda x, y, z, k:
            (x == 'partial_response' and z in ['20-30%', '>30%']) if k == 'yes' 
            else (x == 'partial_response' and z in ['10-20%', '20-30%', '>30%']),
            
        'partial response'+'>30% response': lambda x, y, z, k: x == 'partial_response' and z == '>30%',

        # Stability or Partial Response over time
        'stability or partial response'+'>8 weeks': lambda x, y, z, k: x in ['partial_response', 'stable'] and y in ['8-12', '12-16', '16-24', '24-26', '26-104', '>104'],
        'stability or partial response'+'>12 weeks': lambda x, y, z, k: x in ['partial_response', 'stable'] and y in ['12-16', '16-24', '24-26', '26-104', '>104'],
        'stability or partial response'+'>16 weeks': lambda x, y, z, k: x in ['partial_response', 'stable'] and y in ['12-16', '16-24', '24-26', '26-104', '>104'],
        'stability or partial response'+'>26 weeks': lambda x, y, z, k: x in ['partial_response', 'stable'] and y in ['26-104', '>104'],

        # Progression
        'progression': lambda x, y, z, k: x == 'progression',

        'partial response>104 weeks>30% response' : lambda x, y, z, k: x == 'partial_response' and y == '>104' and z == '>30%',

        # Partial Response and RECIST evaluation
        'partial response'+'>24 weeks'+'>10% RECIST OR >20% after trans-arterial treatment;'*2: lambda x, y, z, k:
            (x == 'partial_response' and y in ['24-26', '26-104', '>104'] and z in ['20-30%', '>30%']) if k == 'yes' 
            else (x == 'partial_response' and y in ['24-26', '26-104', '>104'] and z in ['10-20%', '20-30%', '>30%']),
    },

]

class Dummy:
    def __eq__(self, other):
        return True

    def __ne__(self, other):
        return False

    def __gt__(self, other):
        return True

    def __ge__(self, other):
        return True

    def __lt__(self, other):
        return True

    def __le__(self, other):
        return True

    def __contains__(self, item):
        return True

    def __hash__(self):
        return 0

    def __str__(self):
        return "Dummy"

    def __repr__(self):
        return "Dummy"


query_to_field = [[] for _ in range(len(query_data))]

for i, item in enumerate(fields_data):
    if item.query_id >= 0:
        query_to_field[item.query_id].append(i)

field_to_id = {field.name: i for i, field in enumerate(fields_data)}

