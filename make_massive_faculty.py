import random

departments = ['AI', 'CSE', 'IT', 'ECE', 'EEE', 'MECH', 'CIVIL']

# Generate 350 faculty names
first_names = ["Aarav", "Vivaan", "Aditya", "Vihaan", "Arjun", "Sai", "Rayaan", "Krishna", "Ishaan", "Shaurya", "Atharv", "Ayaan", "Om", "Rishi", "Dhruv", "Ananya", "Aarohi", "Diya", "Prisha", "Avni", "Kavya", "Saanvi", "Aditi", "Isha", "Riya", "Pari", "Anika", "Navya", "Meera", "Zara"]
last_names = ["Sharma", "Verma", "Reddy", "Rao", "Gupta", "Khan", "Nair", "Singh", "Das", "Bose", "Menon", "Iyer", "Patil", "Joshi", "Choudhury", "Mehta", "Kapoor", "Saxena", "Desai", "Acharya", "Pillai", "Shetty", "Ali", "Fernandez", "Naidu", "Qureshi", "Kumar", "Prasad", "Asha", "Ahmad", "Gowda", "Babu", "Mishra", "Pandey"]
titles = ["Dr.", "Prof.", "Mr.", "Ms.", "Mrs."]

# Build faculty pool string
generated_names = set()
faculty_pool = {}

while len(faculty_pool) < 350:
    t = random.choice(titles)
    f = random.choice(first_names)
    l = random.choice(last_names)
    name = f"{t} {f} {l}"
    if name not in generated_names:
        generated_names.add(name)
        fid = str(random.randint(1000, 9999))
        faculty_pool[name] = fid

fp_str = "faculty_pool = {\n"
for k, v in faculty_pool.items():
    fp_str += f"    '{k}': '{v}',\n"
fp_str += "}\n\n"

with open("curriculum_data.py", "r") as f:
    text = f.read()

# Replace faculty_pool
start_idx = text.find("faculty_pool = {")
end_idx = text.find("}", start_idx) + 1
text = text[:start_idx] + fp_str + text[end_idx:]

# Handle first year common subject diversity
def replace_common_s1(match):
    return text

text = text.replace(
    "common_s1 = [",
    "common_s1 = [\n        {'code': f'{dept}1101', 'name': f'Mathematics I ({dept})'},\n        {'code': f'{dept}1102', 'name': f'Physics ({dept})'},\n        {'code': f'{dept}1103', 'name': 'Basic Electrical'},\n        {'code': f'{dept}1104', 'name': 'Engineering Mechanics'},\n        {'code': f'{dept}1105', 'name': 'English'},\n        {'code': f'{dept}1106', 'name': 'Graphics'},\n        {'code': f'{dept}1107', 'name': 'EVS'},\n        {'code': f'{dept}1181', 'name': 'Workshop Lab', 'lab': True},\n    ] #"
)
text = text.replace(
    "common_s2 = [",
    "common_s2 = [\n        {'code': f'{dept}2101', 'name': f'Mathematics II ({dept})'},\n        {'code': f'{dept}2102', 'name': f'Chemistry ({dept})'},\n        {'code': f'{dept}2103', 'name': f'Programming for Problem Solving ({dept})'},\n        {'code': f'{dept}2104', 'name': 'Basic Electronics'},\n        {'code': f'{dept}2105', 'name': 'Thermodynamics'},\n        {'code': f'{dept}2106', 'name': 'Professional Communication'},\n        {'code': f'{dept}2107', 'name': 'Indian Constitution'},\n        {'code': f'{dept}2181', 'name': 'Programming Lab', 'lab': True},\n    ] #"
)

with open("curriculum_data.py", "w") as f:
    f.write(text)

# Also patch seed_curriculum.py
with open("seed_curriculum.py", "r") as f:
    code = f.read()

patch_code = """
    # ------------------------------------------------------------------
    # 8.  Subjects  (per-department, de-duplicated by code per dept)
    #     + FacultySubject assignments
    # ------------------------------------------------------------------
    print("  [8/8] Populating subjects & faculty assignments with STRICT LOAD BALANCING...")

    subject_count = 0
    fs_count = 0
    subject_db_map = {}

    # Track faculty workloads: {faculty_id: {'theory': 0, 'lab': 0}}
    faculty_loads = {f.id: {'theory': 0, 'lab': 0} for f in faculty_db_map.values()}

    for dept_name, branch_name, sections in STRUCTURE:
        dept_obj = dept_db[dept_name]
        
        # Get all faculty belonging to this department
        dept_faculties = [f for key, f in faculty_db_map.items() if f.department_id == dept_obj.id]

        for sem in range(1, 9):
            raw_subjects = get_subjects_for_dept(branch_name, sem)

            for subj in raw_subjects:
                code = subj['code']
                key  = (dept_name, code)
                is_lab = subj.get('lab', False) or any(k in subj['name'].lower() for k in ['lab', 'workshop', 'project', 'viva'])

                # De-duplicate: add subject to DB only once per dept
                if key not in subject_db_map:
                    hrs = get_required_periods(subj)
                    sub_obj = Subject(
                        code=code,
                        name=subj['name'],
                        department_id=dept_obj.id,
                        hours_per_week=hrs
                    )
                    db.session.add(sub_obj)
                    db.session.flush()
                    subject_db_map[key] = sub_obj
                    subject_count += 1

                sub_obj = subject_db_map[key]

                # Assign DIFFERENT faculty for each section for the same subject
                for sec in sections:
                    assigned_fac = None
                    
                    random.shuffle(dept_faculties) # shuffle to balance
                    
                    for fac in dept_faculties:
                        load = faculty_loads[fac.id]
                        if is_lab:
                            if load['lab'] < 3:
                                assigned_fac = fac
                                load['lab'] += 1
                                break
                        else:
                            if load['theory'] < 3:
                                assigned_fac = fac
                                load['theory'] += 1
                                break
                                
                    if not assigned_fac:
                        # Fallback if somehow department faculty is exhausted: use ANY low-load faculty globally
                        all_fac_list = list(faculty_db_map.values())
                        random.shuffle(all_fac_list)
                        for fac in all_fac_list:
                            load = faculty_loads[fac.id]
                            if is_lab and load['lab'] < 3:
                                assigned_fac = fac
                                load['lab'] += 1
                                break
                            elif not is_lab and load['theory'] < 3:
                                assigned_fac = fac
                                load['theory'] += 1
                                break
                    
                    if not assigned_fac:
                        # Absolute emergency fallback, shouldn't happen with 350 faculty
                        assigned_fac = dept_faculties[0]
                        print("WARNING: Faculty over-allocated!")

                    # Avoid duplicate FacultySubject rows (a faculty might be assigned to both sections hypothetically, but we want distinct mapping)
                    exists = FacultySubject.query.filter_by(faculty_id=assigned_fac.id, subject_id=sub_obj.id).first()
                    if not exists:
                        db.session.add(FacultySubject(faculty_id=assigned_fac.id, subject_id=sub_obj.id))
                        fs_count += 1
"""

# Replace the block 8 in seed_curriculum.py
import re
code = re.sub(
    r'# 8\.  Subjects(.*?)db\.session\.commit\(\)',
    patch_code.strip() + "\n    db.session.commit()",
    code,
    flags=re.DOTALL
)

with open("seed_curriculum.py", "w") as f:
    f.write(code)

print("Data successfully updated!")
