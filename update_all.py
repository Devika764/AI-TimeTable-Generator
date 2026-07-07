import os

# 1. Update curriculum_data.py
try:
    with open("curriculum_data.py", "r") as f:
        curr = f.read()

    # Add Comprehensive Viva to Sem 8 of existing branches
    for prefix in ['20AM', '20AD', '20CS', '20IT', '20EC', '20EE']:
        old = f"{{'code': '{prefix}8181', 'name': 'Project Phase II', 'lab': True}},\n            ],"
        new = f"{{'code': '{prefix}8181', 'name': 'Project Phase II', 'lab': True}},\n                {{'code': '{prefix}8182', 'name': 'Comprehensive Viva', 'lab': True}},\n            ],"
        curr = curr.replace(old, new)

    mech_civil = """
        'MECH': {
            3: [
                {'code': '20ME3101', 'name': 'Mathematics for Mechanical'},
                {'code': '20ME3102', 'name': 'Thermodynamics'},
                {'code': '20ME3103', 'name': 'Engineering Mechanics'},
                {'code': '20ME3104', 'name': 'Mechanics of Materials'},
                {'code': '20ME3105', 'name': 'Material Science'},
                {'code': '20ME3181', 'name': 'Thermo Lab', 'lab': True},
                {'code': '20ME3182', 'name': 'Mechanics Lab', 'lab': True},
            ],
            4: [
                {'code': '20ME4101', 'name': 'Fluid Mechanics'},
                {'code': '20ME4102', 'name': 'Kinematics of Machinery'},
                {'code': '20ME4103', 'name': 'Applied Thermodynamics'},
                {'code': '20ME4104', 'name': 'Manufacturing Processes'},
                {'code': '20ME4105', 'name': 'Instrumentation'},
                {'code': '20ME4181', 'name': 'Fluid Mechanics Lab', 'lab': True},
                {'code': '20ME4182', 'name': 'Manufacturing Lab', 'lab': True},
            ],
            5: [
                {'code': '20ME5101', 'name': 'Dynamics of Machinery'},
                {'code': '20ME5102', 'name': 'Heat Transfer'},
                {'code': '20ME5103', 'name': 'Machine Design I'},
                {'code': '20ME5104', 'name': 'Internal Combustion Engines'},
                {'code': '20ME5105', 'name': 'Automation'},
                {'code': '20ME5181', 'name': 'Heat Transfer Lab', 'lab': True},
                {'code': '20ME5182', 'name': 'Machine Dynamics Lab', 'lab': True},
            ],
            6: [
                {'code': '20ME6101', 'name': 'Machine Design II'},
                {'code': '20ME6102', 'name': 'CAD/CAM'},
                {'code': '20ME6103', 'name': 'Automobile Engineering'},
                {'code': '20ME6104', 'name': 'Operations Research'},
                {'code': '20ME6105', 'name': 'Industry Specific Employability Skills'},
                {'code': '20ME6181', 'name': 'CAD/CAM Lab', 'lab': True},
                {'code': '20ME6182', 'name': 'Automobile Lab', 'lab': True},
                {'code': '20HS6101', 'name': 'Technical Paper Writing & IPR'},
                {'code': '20PT6A19', 'name': 'P & T Verbal Ability'},
                {'code': '20PT6C20', 'name': 'P & T Coding'},
            ],
            7: [
                {'code': '20ME7101', 'name': 'Mechatronics'},
                {'code': '20ME7102', 'name': 'Finite Element Analysis'},
                {'code': '20ME7103', 'name': 'Elective I'},
                {'code': '20ME7104', 'name': 'Open Elective I'},
                {'code': '20ME7105', 'name': 'Open Elective II'},
                {'code': '20ME7181', 'name': 'FEA Lab', 'lab': True},
                {'code': '20ME7182', 'name': 'Project Phase I', 'lab': True},
            ],
            8: [
                {'code': '20ME8101', 'name': 'Elective II'},
                {'code': '20ME8102', 'name': 'Elective III'},
                {'code': '20ME8181', 'name': 'Project Phase II', 'lab': True},
                {'code': '20ME8182', 'name': 'Comprehensive Viva', 'lab': True},
            ],
        },
        'CIVIL': {
            3: [
                {'code': '20CE3101', 'name': 'Mathematics for Civil'},
                {'code': '20CE3102', 'name': 'Surveying'},
                {'code': '20CE3103', 'name': 'Engineering Geology'},
                {'code': '20CE3104', 'name': 'Strength of Materials'},
                {'code': '20CE3105', 'name': 'Building Materials'},
                {'code': '20CE3181', 'name': 'Surveying Lab', 'lab': True},
                {'code': '20CE3182', 'name': 'Geology Lab', 'lab': True},
            ],
            4: [
                {'code': '20CE4101', 'name': 'Structural Analysis I'},
                {'code': '20CE4102', 'name': 'Fluid Mechanics for Civil'},
                {'code': '20CE4103', 'name': 'Concrete Technology'},
                {'code': '20CE4104', 'name': 'Transportation Engineering'},
                {'code': '20CE4105', 'name': 'Engineering Economics'},
                {'code': '20CE4181', 'name': 'Materials Lab', 'lab': True},
                {'code': '20CE4182', 'name': 'Fluid Mechanics Lab', 'lab': True},
            ],
            5: [
                {'code': '20CE5101', 'name': 'Structural Analysis II'},
                {'code': '20CE5102', 'name': 'Geotechnical Engineering'},
                {'code': '20CE5103', 'name': 'Water Resources Engineering'},
                {'code': '20CE5104', 'name': 'Environmental Engineering I'},
                {'code': '20CE5105', 'name': 'Estimation and Costing'},
                {'code': '20CE5181', 'name': 'Geotechnical Lab', 'lab': True},
                {'code': '20CE5182', 'name': 'Environmental Lab', 'lab': True},
            ],
            6: [
                {'code': '20CE6101', 'name': 'Design of Steel Structures'},
                {'code': '20CE6102', 'name': 'Foundation Engineering'},
                {'code': '20CE6103', 'name': 'Environmental Engineering II'},
                {'code': '20CE6104', 'name': 'Highway Engineering'},
                {'code': '20CE6105', 'name': 'Industry Specific Employability Skills'},
                {'code': '20CE6181', 'name': 'Steel Detailing Lab', 'lab': True},
                {'code': '20CE6182', 'name': 'Highway Lab', 'lab': True},
                {'code': '20HS6101', 'name': 'Technical Paper Writing & IPR'},
                {'code': '20PT6A19', 'name': 'P & T Verbal Ability'},
                {'code': '20PT6C20', 'name': 'P & T Coding'},
            ],
            7: [
                {'code': '20CE7101', 'name': 'Design of Concrete Structures'},
                {'code': '20CE7102', 'name': 'Construction Management'},
                {'code': '20CE7103', 'name': 'Elective I'},
                {'code': '20CE7104', 'name': 'Open Elective I'},
                {'code': '20CE7105', 'name': 'Open Elective II'},
                {'code': '20CE7181', 'name': 'Concrete Detailing Lab', 'lab': True},
                {'code': '20CE7182', 'name': 'Project Phase I', 'lab': True},
            ],
            8: [
                {'code': '20CE8101', 'name': 'Elective II'},
                {'code': '20CE8102', 'name': 'Elective III'},
                {'code': '20CE8181', 'name': 'Project Phase II', 'lab': True},
                {'code': '20CE8182', 'name': 'Comprehensive Viva', 'lab': True},
            ],
        }"""
    
    curr = curr.replace("        }\n    }", "        },\n" + mech_civil + "\n    }")
    
    branches_old = """department_branches = [
    ('AI', 'AIML', ['A', 'B']),
    ('AI', 'AIDS', ['A', 'B']),
    ('CSE', 'CSE', ['A', 'B', 'C']),
    ('IT', 'IT', ['A', 'B']),
    ('ECE', 'ECE', ['A', 'B', 'C']),
    ('EEE', 'EEE', ['A', 'B']),
]"""
    branches_new = """department_branches = [
    ('AI', 'AIML', ['A', 'B']),
    ('AI', 'AIDS', ['A', 'B']),
    ('CSE', 'CSE', ['A', 'B']),
    ('IT', 'IT', ['A', 'B']),
    ('ECE', 'ECE', ['A', 'B']),
    ('EEE', 'EEE', ['A', 'B']),
    ('MECH', 'MECH', ['A', 'B']),
    ('CIVIL', 'CIVIL', ['A', 'B']),
]"""
    curr = curr.replace(branches_old, branches_new)
    
    abbrs_old = """    if 'electrical' in name: return 'BEE'
    return name[:3].upper()"""
    abbrs_new = """    if 'electrical' in name: return 'BEE'
    if 'thermodynamics' in name: return 'TD'
    if 'fluid mechanics' in name: return 'FM'
    if 'machine design' in name: return 'MD'
    if 'manufacturing' in name: return 'MFG'
    if 'cad/cam' in name: return 'CAD'
    if 'automobile' in name: return 'AUTO'
    if 'mechatronics' in name: return 'MT'
    if 'finite element' in name: return 'FEA'
    if 'surveying' in name: return 'SURV'
    if 'geology' in name: return 'GEOL'
    if 'strength of' in name: return 'SOM'
    if 'structural analysis' in name: return 'SA'
    if 'concrete' in name: return 'CT'
    if 'transportation' in name: return 'TE'
    if 'geotechnical' in name: return 'GTE'
    if 'water resources' in name: return 'WRE'
    if 'steel' in name: return 'DSS'
    if 'foundation' in name: return 'FE'
    if 'viva' in name: return 'VIVA'
    return name[:3].upper()"""
    if abbrs_old in curr:
        curr = curr.replace(abbrs_old, abbrs_new)
    
    curr = curr.replace("'lab' in name or 'project' in name or 'workshop' in name", "'lab' in name or 'project' in name or 'workshop' in name or 'viva' in name")
    
    with open("curriculum_data.py", "w") as f:
        f.write(curr)

    # 2. Update seed_curriculum.py
    with open("seed_curriculum.py", "r") as f:
        seed = f.read()

    seed_struct_old = """STRUCTURE = [
    ('AI',  'AIML', ['A', 'B']),
    ('AI',  'AIDS', ['A', 'B']),
    ('CSE', 'CSE',  ['A', 'B', 'C']),
    ('IT',  'IT',   ['A', 'B']),
    ('ECE', 'ECE',  ['A', 'B', 'C']),
    ('EEE', 'EEE',  ['A', 'B']),
]"""
    seed_struct_new = """STRUCTURE = [
    ('AI',  'AIML', ['A', 'B']),
    ('AI',  'AIDS', ['A', 'B']),
    ('CSE', 'CSE',  ['A', 'B']),
    ('IT',  'IT',   ['A', 'B']),
    ('ECE', 'ECE',  ['A', 'B']),
    ('EEE', 'EEE',  ['A', 'B']),
    ('MECH', 'MECH', ['A', 'B']),
    ('CIVIL', 'CIVIL', ['A', 'B']),
]"""
    seed = seed.replace(seed_struct_old, seed_struct_new)
    seed = seed.replace("DEPT_NAMES = ['AI', 'CSE', 'IT', 'ECE', 'EEE']", "DEPT_NAMES = ['AI', 'CSE', 'IT', 'ECE', 'EEE', 'MECH', 'CIVIL']")
    
    with open("seed_curriculum.py", "w") as f:
        f.write(seed)

    # 3. Update ai_module.py
    with open("ai_module.py", "r") as f:
        aimod = f.read()
    aimod = aimod.replace("['lab', 'workshop', 'graphics', 'drawing', 'project']", "['lab', 'workshop', 'graphics', 'drawing', 'project', 'viva']")
    with open("ai_module.py", "w") as f:
        f.write(aimod)

    print("Successfully patched Python files for MECH and CIVIL and 2 sections each!")
except Exception as e:
    print(f"Error: {e}")
