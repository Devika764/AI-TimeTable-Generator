# curriculum_data.py
# Full dataset for multiple departments: AI (AIML, AIDS), CSE, IT, ECE, EEE
# 8 semesters, each with given sections.
# Room numbers from 1201 to 1299 (cyclic)

# ----------------------------------------------------------------------
# Faculty Pool (with IDs) – expanded to cover many subjects
# ----------------------------------------------------------------------
faculty_pool = {
    'Dr. Aditya Singh': '4556',
    'Ms. Vivaan Mehta': '8416',
    'Ms. Ayaan Rao': '3294',
    'Ms. Krishna Das': '1298',
    'Prof. Saanvi Joshi': '2665',
    'Mrs. Shaurya Saxena': '5074',
    'Mr. Vihaan Pillai': '7998',
    'Mrs. Isha Singh': '5925',
    'Mr. Aarav Qureshi': '9889',
    'Ms. Isha Menon': '1905',
    'Mrs. Atharv Reddy': '8864',
    'Mrs. Ayaan Desai': '1191',
    'Mrs. Riya Khan': '3914',
    'Prof. Rayaan Patil': '5020',
    'Mr. Aditi Sharma': '5015',
    'Mr. Pari Das': '3968',
    'Ms. Anika Joshi': '6299',
    'Prof. Aditi Singh': '7039',
    'Dr. Sai Choudhury': '2101',
    'Dr. Diya Qureshi': '3512',
    'Dr. Diya Kapoor': '7717',
    'Prof. Shaurya Bose': '6976',
    'Ms. Aditya Kapoor': '9290',
    'Mrs. Saanvi Kapoor': '1029',
    'Dr. Vivaan Asha': '7714',
    'Dr. Aditi Singh': '1152',
    'Prof. Aditi Ali': '7761',
    'Dr. Om Naidu': '8364',
    'Prof. Sai Shetty': '2802',
    'Dr. Atharv Ali': '6596',
    'Prof. Kavya Kapoor': '4449',
    'Ms. Vivaan Iyer': '1035',
    'Mrs. Aarohi Fernandez': '9340',
    'Mrs. Isha Mehta': '7618',
    'Mr. Atharv Sharma': '6478',
    'Prof. Aditya Gowda': '9613',
    'Mrs. Aarav Mishra': '5826',
    'Prof. Anika Acharya': '4858',
    'Mr. Ananya Naidu': '8576',
    'Mr. Anika Gowda': '6963',
    'Mr. Vivaan Choudhury': '8360',
    'Prof. Riya Pillai': '2172',
    'Prof. Om Acharya': '9601',
    'Mr. Prisha Fernandez': '1680',
    'Mr. Navya Fernandez': '3783',
    'Mr. Prisha Khan': '7722',
    'Dr. Dhruv Rao': '9031',
    'Dr. Dhruv Naidu': '2029',
    'Mrs. Sai Sharma': '5437',
    'Prof. Meera Reddy': '1374',
    'Prof. Ishaan Mishra': '4716',
    'Mrs. Om Singh': '2868',
    'Mrs. Om Naidu': '5716',
    'Mrs. Saanvi Singh': '8618',
    'Ms. Shaurya Ali': '3367',
    'Ms. Om Singh': '1637',
    'Mr. Aarav Patil': '2588',
    'Ms. Prisha Saxena': '8717',
    'Ms. Ayaan Reddy': '8300',
    'Mrs. Krishna Reddy': '5819',
    'Ms. Saanvi Bose': '9518',
    'Mrs. Shaurya Fernandez': '5366',
    'Prof. Prisha Singh': '3188',
    'Mrs. Ishaan Mishra': '2372',
    'Dr. Diya Fernandez': '7845',
    'Dr. Dhruv Babu': '9055',
    'Prof. Arjun Fernandez': '7147',
    'Ms. Aarav Joshi': '3182',
    'Mrs. Diya Kapoor': '8282',
    'Mrs. Riya Naidu': '4981',
    'Dr. Pari Mishra': '7407',
    'Prof. Vihaan Ali': '6252',
    'Ms. Anika Acharya': '8900',
    'Dr. Navya Saxena': '6848',
    'Mr. Aarav Pandey': '2375',
    'Ms. Ishaan Pandey': '4919',
    'Ms. Aarohi Ali': '5694',
    'Mrs. Riya Gowda': '1576',
    'Mr. Krishna Asha': '3463',
    'Dr. Ishaan Verma': '8020',
    'Ms. Rayaan Qureshi': '3179',
    'Prof. Sai Kumar': '8983',
    'Mrs. Aditi Mishra': '2193',
    'Prof. Anika Babu': '6504',
    'Mr. Kavya Gupta': '2135',
    'Mrs. Dhruv Ahmad': '6370',
    'Prof. Avni Joshi': '6767',
    'Dr. Sai Desai': '9593',
    'Dr. Aarav Pandey': '8523',
    'Mr. Aarohi Verma': '3589',
    'Prof. Arjun Shetty': '6279',
    'Prof. Rayaan Reddy': '1907',
    'Mr. Avni Khan': '9165',
    'Ms. Atharv Mehta': '8419',
    'Dr. Pari Desai': '7681',
    'Dr. Prisha Kapoor': '8141',
    'Dr. Rishi Qureshi': '4495',
    'Dr. Aditya Fernandez': '8869',
    'Ms. Aarav Mehta': '7202',
    'Ms. Meera Khan': '6039',
    'Prof. Sai Khan': '8563',
    'Mrs. Prisha Acharya': '6486',
    'Dr. Dhruv Ahmad': '2702',
    'Mrs. Rishi Kumar': '1251',
    'Mr. Om Mishra': '8842',
    'Prof. Ishaan Babu': '5671',
    'Dr. Diya Kumar': '6809',
    'Mrs. Kavya Verma': '3333',
    'Mrs. Dhruv Patil': '6244',
    'Mrs. Om Joshi': '7200',
    'Ms. Ananya Verma': '7656',
    'Ms. Om Choudhury': '4659',
    'Ms. Pari Reddy': '4504',
    'Mr. Krishna Naidu': '7465',
    'Mrs. Ishaan Sharma': '5547',
    'Mrs. Krishna Iyer': '1469',
    'Prof. Zara Verma': '4725',
    'Ms. Arjun Patil': '8644',
    'Prof. Aditi Ahmad': '3269',
    'Dr. Avni Joshi': '7986',
    'Mr. Ishaan Mehta': '7118',
    'Mrs. Ayaan Mishra': '1036',
    'Ms. Sai Gowda': '5256',
    'Mrs. Atharv Das': '1833',
    'Mr. Isha Patil': '6835',
    'Mr. Sai Menon': '1836',
    'Dr. Aditi Desai': '1713',
    'Mr. Avni Mishra': '8382',
    'Dr. Rayaan Mishra': '6810',
    'Ms. Kavya Kapoor': '5413',
    'Ms. Rayaan Naidu': '4865',
    'Dr. Ishaan Babu': '8825',
    'Ms. Ishaan Qureshi': '2418',
    'Mr. Ishaan Sharma': '1409',
    'Mr. Dhruv Prasad': '8702',
    'Mr. Riya Reddy': '4179',
    'Dr. Prisha Pillai': '8155',
    'Ms. Aditi Naidu': '9470',
    'Prof. Avni Saxena': '1661',
    'Dr. Dhruv Asha': '2636',
    'Mr. Ananya Joshi': '2094',
    'Mr. Rayaan Ahmad': '4601',
    'Ms. Aarohi Saxena': '1541',
    'Mrs. Vivaan Acharya': '8494',
    'Ms. Avni Rao': '3472',
    'Prof. Om Joshi': '2182',
    'Dr. Aditi Das': '9689',
    'Ms. Pari Shetty': '4879',
    'Dr. Vivaan Prasad': '5934',
    'Mrs. Ananya Ahmad': '8206',
    'Mr. Atharv Patil': '2317',
    'Prof. Pari Naidu': '3451',
    'Mrs. Aditi Saxena': '4464',
    'Dr. Rishi Khan': '8560',
    'Ms. Shaurya Mishra': '5633',
    'Dr. Rayaan Babu': '8498',
    'Dr. Vivaan Babu': '9605',
    'Mrs. Vivaan Fernandez': '2040',
    'Ms. Sai Khan': '5112',
    'Prof. Vihaan Singh': '4885',
    'Prof. Dhruv Kumar': '5305',
    'Dr. Om Reddy': '6456',
    'Prof. Aarav Singh': '6693',
    'Prof. Ananya Naidu': '6273',
    'Mrs. Avni Das': '5206',
    'Mr. Ayaan Pandey': '2769',
    'Prof. Aarohi Gupta': '7175',
    'Prof. Atharv Acharya': '9108',
    'Ms. Zara Babu': '3414',
    'Ms. Dhruv Desai': '5806',
    'Prof. Rishi Ahmad': '1575',
    'Mrs. Kavya Shetty': '8513',
    'Prof. Pari Bose': '5206',
    'Ms. Diya Gupta': '2071',
    'Prof. Vivaan Choudhury': '6457',
    'Ms. Rayaan Babu': '6711',
    'Ms. Aarohi Desai': '8937',
    'Ms. Isha Asha': '9863',
    'Ms. Vivaan Qureshi': '1081',
    'Mr. Sai Mishra': '6078',
    'Dr. Om Khan': '8622',
    'Dr. Kavya Qureshi': '2487',
    'Mr. Sai Shetty': '8170',
    'Mrs. Kavya Khan': '8278',
    'Prof. Aditi Qureshi': '9937',
    'Dr. Rishi Babu': '6231',
    'Ms. Isha Qureshi': '1924',
    'Ms. Sai Naidu': '4105',
    'Mrs. Pari Khan': '7785',
    'Prof. Meera Patil': '8432',
    'Mr. Aditya Saxena': '8000',
    'Ms. Aarohi Gowda': '6839',
    'Prof. Aarohi Joshi': '3409',
    'Dr. Om Sharma': '2809',
    'Ms. Diya Bose': '7834',
    'Prof. Krishna Rao': '4871',
    'Dr. Rishi Gowda': '6686',
    'Mrs. Aditi Gowda': '4869',
    'Mrs. Ananya Acharya': '7842',
    'Mrs. Saanvi Gupta': '4608',
    'Mr. Saanvi Verma': '7646',
    'Mrs. Arjun Fernandez': '2943',
    'Mr. Om Kumar': '3415',
    'Prof. Ananya Ahmad': '3737',
    'Ms. Sai Verma': '5553',
    'Dr. Shaurya Saxena': '4233',
    'Ms. Navya Shetty': '5112',
    'Mr. Rishi Verma': '3108',
    'Dr. Vivaan Qureshi': '1447',
    'Mrs. Atharv Nair': '3292',
    'Prof. Rayaan Fernandez': '4026',
    'Prof. Om Babu': '4380',
    'Mr. Kavya Mishra': '2563',
    'Ms. Prisha Sharma': '1547',
    'Prof. Kavya Nair': '8273',
    'Mr. Aarav Asha': '4416',
    'Mrs. Saanvi Babu': '9226',
    'Mr. Zara Saxena': '2772',
    'Prof. Pari Khan': '5103',
    'Prof. Prisha Gowda': '1099',
    'Prof. Kavya Mishra': '2082',
    'Mrs. Diya Kumar': '7519',
    'Dr. Anika Naidu': '7833',
    'Dr. Prisha Ali': '7601',
    'Mr. Arjun Sharma': '9202',
    'Mrs. Shaurya Verma': '2369',
    'Mrs. Riya Menon': '8510',
    'Mr. Krishna Kapoor': '5245',
    'Ms. Om Qureshi': '3657',
    'Ms. Saanvi Ali': '8856',
    'Mrs. Isha Mishra': '8806',
    'Mrs. Prisha Qureshi': '4500',
    'Dr. Om Das': '4460',
    'Ms. Dhruv Mishra': '8086',
    'Prof. Ananya Khan': '5833',
    'Ms. Om Nair': '4016',
    'Dr. Ayaan Reddy': '6040',
    'Mrs. Dhruv Das': '6825',
    'Ms. Saanvi Mishra': '2457',
    'Ms. Atharv Acharya': '4766',
    'Dr. Avni Mehta': '3161',
    'Mr. Aditi Pandey': '1527',
    'Mr. Anika Khan': '8179',
    'Dr. Zara Babu': '9372',
    'Dr. Diya Mehta': '6397',
    'Prof. Aditi Naidu': '1938',
    'Mr. Rayaan Nair': '3530',
    'Mr. Ayaan Gowda': '3937',
    'Mr. Rayaan Kapoor': '1345',
    'Mr. Atharv Reddy': '6523',
    'Ms. Sai Patil': '1047',
    'Mr. Diya Gowda': '9497',
    'Ms. Diya Patil': '6495',
    'Ms. Sai Gupta': '4787',
    'Prof. Om Mehta': '5523',
    'Mrs. Navya Gowda': '8837',
    'Mr. Aditya Menon': '4046',
    'Dr. Isha Shetty': '4836',
    'Prof. Ishaan Shetty': '2343',
    'Ms. Meera Reddy': '1021',
    'Mr. Avni Gowda': '5423',
    'Ms. Avni Gupta': '5994',
    'Mr. Arjun Khan': '5612',
    'Mrs. Diya Qureshi': '3556',
    'Mrs. Sai Nair': '6746',
    'Mr. Saanvi Fernandez': '6264',
    'Ms. Meera Das': '8282',
    'Prof. Ayaan Choudhury': '6557',
    'Mrs. Zara Shetty': '4294',
    'Mrs. Meera Qureshi': '2396',
    'Mr. Avni Rao': '1790',
    'Ms. Sai Joshi': '3602',
    'Ms. Arjun Choudhury': '1011',
    'Dr. Arjun Pillai': '7845',
    'Mrs. Anika Choudhury': '8630',
    'Prof. Prisha Pandey': '7391',
    'Prof. Arjun Kapoor': '8909',
    'Mrs. Pari Naidu': '9115',
    'Prof. Isha Sharma': '7042',
    'Mr. Ishaan Naidu': '4815',
    'Mr. Aarohi Singh': '8396',
    'Mrs. Vivaan Ali': '1634',
    'Prof. Vihaan Asha': '4351',
    'Ms. Arjun Mishra': '1051',
    'Mr. Aarav Kapoor': '9665',
    'Mr. Rayaan Kumar': '3158',
    'Mrs. Ananya Mehta': '8239',
    'Mrs. Krishna Das': '1769',
    'Prof. Aditya Patil': '5277',
    'Prof. Prisha Naidu': '8630',
    'Dr. Zara Reddy': '6222',
    'Mrs. Pari Verma': '1416',
    'Mr. Aditi Babu': '2572',
    'Ms. Rayaan Das': '7305',
    'Mr. Shaurya Kumar': '4011',
    'Prof. Isha Verma': '5204',
    'Ms. Shaurya Das': '3006',
    'Mr. Riya Singh': '9173',
    'Ms. Arjun Desai': '9405',
    'Ms. Om Babu': '7275',
    'Ms. Avni Nair': '1988',
    'Mr. Pari Shetty': '2535',
    'Prof. Dhruv Joshi': '2780',
    'Prof. Om Shetty': '1129',
    'Mr. Avni Saxena': '8373',
    'Dr. Arjun Iyer': '2339',
    'Mr. Prisha Prasad': '3963',
    'Mrs. Riya Gupta': '9355',
    'Ms. Shaurya Acharya': '9121',
    'Mrs. Meera Rao': '6368',
    'Prof. Pari Mehta': '4827',
    'Mrs. Aarav Acharya': '1366',
    'Mr. Vivaan Kumar': '4325',
    'Ms. Zara Patil': '2572',
    'Dr. Ishaan Mishra': '7780',
    'Ms. Navya Kapoor': '6338',
    'Dr. Vihaan Singh': '1248',
    'Mr. Aarohi Nair': '7668',
    'Ms. Ananya Desai': '2606',
    'Mr. Vihaan Menon': '4602',
    'Mrs. Meera Choudhury': '4562',
    'Prof. Aditi Verma': '9159',
    'Mrs. Ishaan Babu': '7312',
    'Prof. Vihaan Mehta': '7644',
    'Prof. Rishi Mehta': '4711',
    'Dr. Ayaan Fernandez': '8752',
    'Ms. Aarohi Gupta': '3597',
    'Dr. Ayaan Singh': '9624',
    'Mr. Pari Nair': '6885',
    'Mr. Dhruv Kumar': '9946',
    'Mrs. Prisha Sharma': '4383',
    'Mr. Vihaan Mehta': '2132',
    'Mr. Rayaan Pillai': '3536',
    'Ms. Ishaan Patil': '2794',
    'Prof. Kavya Ahmad': '9914',
    'Ms. Meera Shetty': '1938',
    'Ms. Rishi Das': '1497',
    'Ms. Dhruv Mehta': '4669',
    'Prof. Arjun Prasad': '6577',
    'Ms. Aarav Fernandez': '2859',
    'Ms. Kavya Naidu': '1045',
    'Prof. Krishna Gowda': '4331',
    'Prof. Navya Shetty': '5690',
    'Dr. Isha Fernandez': '2943',
    'Prof. Prisha Asha': '1196',
    'Prof. Diya Pillai': '1546',
    'Ms. Sai Desai': '8261',
    'Ms. Prisha Patil': '7866',
    'Ms. Isha Nair': '4515',
    'Mr. Kavya Pillai': '9165',
}



# ----------------------------------------------------------------------
# Subject definitions per semester for each department
# Semesters 1-2 are common across all branches (can be customized per dept)
# ----------------------------------------------------------------------

def get_subjects_for_dept(dept, semester):
    """
    Return a list of subject dicts for a given department and semester.
    Each subject has: code, name, (optional) lab.
    """
    # Base common subjects for first two semesters (can be same for all)
    common_s1 = [
        {'code': f'{dept}1101', 'name': f'Mathematics I ({dept})'},
        {'code': f'{dept}1102', 'name': f'Physics ({dept})'},
        {'code': f'{dept}1103', 'name': 'Basic Electrical'},
        {'code': f'{dept}1104', 'name': 'Engineering Mechanics'},
        {'code': f'{dept}1105', 'name': 'English'},
        {'code': f'{dept}1106', 'name': 'Graphics'},
        {'code': f'{dept}1107', 'name': 'EVS'},
        {'code': f'{dept}1181', 'name': 'Workshop Lab', 'lab': True},
    ]

    common_s2 = [
        {'code': f'{dept}2101', 'name': f'Mathematics II ({dept})'},
        {'code': f'{dept}2102', 'name': f'Chemistry ({dept})'},
        {'code': f'{dept}2103', 'name': f'Programming for Problem Solving ({dept})'},
        {'code': f'{dept}2104', 'name': 'Basic Electronics'},
        {'code': f'{dept}2105', 'name': 'Thermodynamics'},
        {'code': f'{dept}2106', 'name': 'Professional Communication'},
        {'code': f'{dept}2107', 'name': 'Indian Constitution'},
        {'code': f'{dept}2181', 'name': 'Programming Lab', 'lab': True},
    ]

    dept_subjects = {
        'AIML': {
            3: [
                {'code': '20AM3101', 'name': 'Discrete Mathematics'},
                {'code': '20AM3102', 'name': 'Data Structures'},
                {'code': '20AM3103', 'name': 'Digital Logic Design'},
                {'code': '20AM3104', 'name': 'Computer Organization'},
                {'code': '20AM3105', 'name': 'Object Oriented Programming'},
                {'code': '20AM3181', 'name': 'Data Structures Lab', 'lab': True},
                {'code': '20AM3182', 'name': 'OOP Lab', 'lab': True},
            ],
            4: [
                {'code': '20AM4101', 'name': 'Probability and Statistics'},
                {'code': '20AM4102', 'name': 'Design and Analysis of Algorithms'},
                {'code': '20AM4103', 'name': 'Operating Systems'},
                {'code': '20AM4104', 'name': 'Microprocessors'},
                {'code': '20AM4105', 'name': 'Python Programming'},
                {'code': '20AM4181', 'name': 'OS Lab', 'lab': True},
                {'code': '20AM4182', 'name': 'Python Lab', 'lab': True},
            ],
            5: [
                {'code': '20AM5101', 'name': 'Machine Learning'},
                {'code': '20AM5102', 'name': 'Computer Networks'},
                {'code': '20AM5103', 'name': 'Artificial Intelligence'},
                {'code': '20AM5104', 'name': 'Web Technologies'},
                {'code': '20AM5105', 'name': 'Software Engineering'},
                {'code': '20AM5181', 'name': 'Machine Learning Lab', 'lab': True},
                {'code': '20AM5182', 'name': 'Networks Lab', 'lab': True},
            ],
            6: [
                {'code': '20AM6101', 'name': 'Deep Learning'},
                {'code': '20AM6102', 'name': 'Reinforcement Learning'},
                {'code': '20AM6103', 'name': 'Cloud Computing'},
                {'code': '20AM6104', 'name': 'Natural Language Processing'},
                {'code': '20AM6105', 'name': 'Industry Specific Employability Skills'},
                {'code': '20AM6181', 'name': 'Deep Learning Lab', 'lab': True},
                {'code': '20AM6182', 'name': 'Cloud Computing Lab', 'lab': True},
                {'code': '20HS6101', 'name': 'Technical Paper Writing & IPR'},
                {'code': '20PT6A19', 'name': 'P & T Verbal Ability'},
                {'code': '20PT6C20', 'name': 'P & T Coding'},
            ],
            7: [
                {'code': '20AM7101', 'name': 'Elective I'},
                {'code': '20AM7102', 'name': 'Elective II'},
                {'code': '20AM7103', 'name': 'Elective III'},
                {'code': '20AM7104', 'name': 'Open Elective I'},
                {'code': '20AM7105', 'name': 'Open Elective II'},
                {'code': '20AM7181', 'name': 'Elective Lab', 'lab': True},
                {'code': '20AM7182', 'name': 'Project Phase I', 'lab': True},
            ],
            8: [
                {'code': '20AM8101', 'name': 'Elective IV'},
                {'code': '20AM8102', 'name': 'Elective V'},
                {'code': '20AM8181', 'name': 'Project Phase II', 'lab': True},
                {'code': '20AM8182', 'name': 'Comprehensive Viva', 'lab': True},
            ],
        },
        'AIDS': {
            3: [
                {'code': '20AD3101', 'name': 'Discrete Mathematics'},
                {'code': '20AD3102', 'name': 'Data Structures'},
                {'code': '20AD3103', 'name': 'Database Management Systems'},
                {'code': '20AD3104', 'name': 'Computer Organization'},
                {'code': '20AD3105', 'name': 'Object Oriented Programming'},
                {'code': '20AD3181', 'name': 'Data Structures Lab', 'lab': True},
                {'code': '20AD3182', 'name': 'DBMS Lab', 'lab': True},
            ],
            4: [
                {'code': '20AD4101', 'name': 'Probability and Statistics'},
                {'code': '20AD4102', 'name': 'Design and Analysis of Algorithms'},
                {'code': '20AD4103', 'name': 'Operating Systems'},
                {'code': '20AD4104', 'name': 'Data Warehousing'},
                {'code': '20AD4105', 'name': 'Python Programming'},
                {'code': '20AD4181', 'name': 'OS Lab', 'lab': True},
                {'code': '20AD4182', 'name': 'Python Lab', 'lab': True},
            ],
            5: [
                {'code': '20AD5101', 'name': 'Machine Learning'},
                {'code': '20AD5102', 'name': 'Computer Networks'},
                {'code': '20AD5103', 'name': 'Big Data Analytics'},
                {'code': '20AD5104', 'name': 'Web Technologies'},
                {'code': '20AD5105', 'name': 'Data Visualization'},
                {'code': '20AD5181', 'name': 'Machine Learning Lab', 'lab': True},
                {'code': '20AD5182', 'name': 'Big Data Lab', 'lab': True},
            ],
            6: [
                {'code': '20AD6101', 'name': 'Deep Learning'},
                {'code': '20AD6102', 'name': 'Computer Vision'},
                {'code': '20AD6103', 'name': 'Cloud Computing'},
                {'code': '20AD6104', 'name': 'Data Mining'},
                {'code': '20AD6105', 'name': 'Industry Specific Employability Skills'},
                {'code': '20AD6181', 'name': 'Deep Learning Lab', 'lab': True},
                {'code': '20AD6182', 'name': 'Data Mining Lab', 'lab': True},
                {'code': '20HS6101', 'name': 'Technical Paper Writing & IPR'},
                {'code': '20PT6A19', 'name': 'P & T Verbal Ability'},
                {'code': '20PT6C20', 'name': 'P & T Coding'},
            ],
            7: [
                {'code': '20AD7101', 'name': 'Elective I'},
                {'code': '20AD7102', 'name': 'Elective II'},
                {'code': '20AD7103', 'name': 'Elective III'},
                {'code': '20AD7104', 'name': 'Open Elective I'},
                {'code': '20AD7105', 'name': 'Open Elective II'},
                {'code': '20AD7181', 'name': 'Elective Lab', 'lab': True},
                {'code': '20AD7182', 'name': 'Project Phase I', 'lab': True},
            ],
            8: [
                {'code': '20AD8101', 'name': 'Elective IV'},
                {'code': '20AD8102', 'name': 'Elective V'},
                {'code': '20AD8181', 'name': 'Project Phase II', 'lab': True},
                {'code': '20AD8182', 'name': 'Comprehensive Viva', 'lab': True},
            ],
        },
        'CSE': {
            3: [
                {'code': '20CS3101', 'name': 'Discrete Structures'},
                {'code': '20CS3102', 'name': 'Data Structures'},
                {'code': '20CS3103', 'name': 'Digital Logic Design'},
                {'code': '20CS3104', 'name': 'Computer Organization'},
                {'code': '20CS3105', 'name': 'Object Oriented Programming'},
                {'code': '20CS3181', 'name': 'Data Structures Lab', 'lab': True},
                {'code': '20CS3182', 'name': 'OOP Lab', 'lab': True},
            ],
            4: [
                {'code': '20CS4101', 'name': 'Probability and Statistics'},
                {'code': '20CS4102', 'name': 'Design and Analysis of Algorithms'},
                {'code': '20CS4103', 'name': 'Operating Systems'},
                {'code': '20CS4104', 'name': 'Microprocessors'},
                {'code': '20CS4105', 'name': 'Python Programming'},
                {'code': '20CS4181', 'name': 'OS Lab', 'lab': True},
                {'code': '20CS4182', 'name': 'Python Lab', 'lab': True},
            ],
            5: [
                {'code': '20CS5101', 'name': 'Database Management Systems'},
                {'code': '20CS5102', 'name': 'Computer Networks'},
                {'code': '20CS5103', 'name': 'Software Engineering'},
                {'code': '20CS5104', 'name': 'Web Technologies'},
                {'code': '20CS5105', 'name': 'Theory of Computation'},
                {'code': '20CS5181', 'name': 'DBMS Lab', 'lab': True},
                {'code': '20CS5182', 'name': 'Networks Lab', 'lab': True},
            ],
            6: [
                {'code': '20CS6101', 'name': 'Machine Learning'},
                {'code': '20CS6102', 'name': 'Compiler Design'},
                {'code': '20CS6103', 'name': 'Cloud Computing'},
                {'code': '20CS6104', 'name': 'Information Security'},
                {'code': '20CS6105', 'name': 'Industry Specific Employability Skills'},
                {'code': '20CS6181', 'name': 'Machine Learning Lab', 'lab': True},
                {'code': '20CS6182', 'name': 'Cloud Computing Lab', 'lab': True},
                {'code': '20HS6101', 'name': 'Technical Paper Writing & IPR'},
                {'code': '20PT6A19', 'name': 'P & T Verbal Ability'},
                {'code': '20PT6C20', 'name': 'P & T Coding'},
            ],
            7: [
                {'code': '20CS7101', 'name': 'Elective I'},
                {'code': '20CS7102', 'name': 'Elective II'},
                {'code': '20CS7103', 'name': 'Elective III'},
                {'code': '20CS7104', 'name': 'Open Elective I'},
                {'code': '20CS7105', 'name': 'Open Elective II'},
                {'code': '20CS7181', 'name': 'Elective Lab', 'lab': True},
                {'code': '20CS7182', 'name': 'Project Phase I', 'lab': True},
            ],
            8: [
                {'code': '20CS8101', 'name': 'Elective IV'},
                {'code': '20CS8102', 'name': 'Elective V'},
                {'code': '20CS8181', 'name': 'Project Phase II', 'lab': True},
                {'code': '20CS8182', 'name': 'Comprehensive Viva', 'lab': True},
            ],
        },
        'IT': {
            3: [
                {'code': '20IT3101', 'name': 'Discrete Structures'},
                {'code': '20IT3102', 'name': 'Data Structures'},
                {'code': '20IT3103', 'name': 'Digital Logic Design'},
                {'code': '20IT3104', 'name': 'Computer Organization'},
                {'code': '20IT3105', 'name': 'Object Oriented Programming'},
                {'code': '20IT3181', 'name': 'Data Structures Lab', 'lab': True},
                {'code': '20IT3182', 'name': 'OOP Lab', 'lab': True},
            ],
            4: [
                {'code': '20IT4101', 'name': 'Probability and Statistics'},
                {'code': '20IT4102', 'name': 'Design and Analysis of Algorithms'},
                {'code': '20IT4103', 'name': 'Operating Systems'},
                {'code': '20IT4104', 'name': 'Database Management Systems'},
                {'code': '20IT4105', 'name': 'Python Programming'},
                {'code': '20IT4181', 'name': 'OS Lab', 'lab': True},
                {'code': '20IT4182', 'name': 'Python Lab', 'lab': True},
            ],
            5: [
                {'code': '20IT5101', 'name': 'Computer Networks'},
                {'code': '20IT5102', 'name': 'Web Technologies'},
                {'code': '20IT5103', 'name': 'Software Engineering'},
                {'code': '20IT5104', 'name': 'Information Security'},
                {'code': '20IT5105', 'name': 'Data Mining'},
                {'code': '20IT5181', 'name': 'Networks Lab', 'lab': True},
                {'code': '20IT5182', 'name': 'Web Technologies Lab', 'lab': True},
            ],
            6: [
                {'code': '20IT6101', 'name': 'Machine Learning'},
                {'code': '20IT6102', 'name': 'Cloud Computing'},
                {'code': '20IT6103', 'name': 'Big Data Analytics'},
                {'code': '20IT6104', 'name': 'Mobile Computing'},
                {'code': '20IT6105', 'name': 'Industry Specific Employability Skills'},
                {'code': '20IT6181', 'name': 'Machine Learning Lab', 'lab': True},
                {'code': '20IT6182', 'name': 'Cloud Computing Lab', 'lab': True},
                {'code': '20HS6101', 'name': 'Technical Paper Writing & IPR'},
                {'code': '20PT6A19', 'name': 'P & T Verbal Ability'},
                {'code': '20PT6C20', 'name': 'P & T Coding'},
            ],
            7: [
                {'code': '20IT7101', 'name': 'Elective I'},
                {'code': '20IT7102', 'name': 'Elective II'},
                {'code': '20IT7103', 'name': 'Elective III'},
                {'code': '20IT7104', 'name': 'Open Elective I'},
                {'code': '20IT7105', 'name': 'Open Elective II'},
                {'code': '20IT7181', 'name': 'Elective Lab', 'lab': True},
                {'code': '20IT7182', 'name': 'Project Phase I', 'lab': True},
            ],
            8: [
                {'code': '20IT8101', 'name': 'Elective IV'},
                {'code': '20IT8102', 'name': 'Elective V'},
                {'code': '20IT8181', 'name': 'Project Phase II', 'lab': True},
                {'code': '20IT8182', 'name': 'Comprehensive Viva', 'lab': True},
            ],
        },
        'ECE': {
            3: [
                {'code': '20EC3101', 'name': 'Mathematics III'},
                {'code': '20EC3102', 'name': 'Electronic Devices'},
                {'code': '20EC3103', 'name': 'Digital Logic Design'},
                {'code': '20EC3104', 'name': 'Network Theory'},
                {'code': '20EC3105', 'name': 'Signals and Systems'},
                {'code': '20EC3181', 'name': 'Electronics Lab', 'lab': True},
                {'code': '20EC3182', 'name': 'Digital Lab', 'lab': True},
            ],
            4: [
                {'code': '20EC4101', 'name': 'Analog Circuits'},
                {'code': '20EC4102', 'name': 'Control Systems'},
                {'code': '20EC4103', 'name': 'Communication Systems'},
                {'code': '20EC4104', 'name': 'Electromagnetic Theory'},
                {'code': '20EC4105', 'name': 'Microprocessors'},
                {'code': '20EC4181', 'name': 'Analog Lab', 'lab': True},
                {'code': '20EC4182', 'name': 'Microprocessor Lab', 'lab': True},
            ],
            5: [
                {'code': '20EC5101', 'name': 'Digital Signal Processing'},
                {'code': '20EC5102', 'name': 'VLSI Design'},
                {'code': '20EC5103', 'name': 'Antennas and Propagation'},
                {'code': '20EC5104', 'name': 'Embedded Systems'},
                {'code': '20EC5105', 'name': 'Optical Communication'},
                {'code': '20EC5181', 'name': 'DSP Lab', 'lab': True},
                {'code': '20EC5182', 'name': 'VLSI Lab', 'lab': True},
            ],
            6: [
                {'code': '20EC6101', 'name': 'Wireless Communication'},
                {'code': '20EC6102', 'name': 'Microwave Engineering'},
                {'code': '20EC6103', 'name': 'Digital Image Processing'},
                {'code': '20EC6104', 'name': 'RF Circuit Design'},
                {'code': '20EC6105', 'name': 'Industry Specific Employability Skills'},
                {'code': '20EC6181', 'name': 'Communication Lab', 'lab': True},
                {'code': '20EC6182', 'name': 'Microwave Lab', 'lab': True},
                {'code': '20HS6101', 'name': 'Technical Paper Writing & IPR'},
                {'code': '20PT6A19', 'name': 'P & T Verbal Ability'},
                {'code': '20PT6C20', 'name': 'P & T Coding'},
            ],
            7: [
                {'code': '20EC7101', 'name': 'Elective I'},
                {'code': '20EC7102', 'name': 'Elective II'},
                {'code': '20EC7103', 'name': 'Elective III'},
                {'code': '20EC7104', 'name': 'Open Elective I'},
                {'code': '20EC7105', 'name': 'Open Elective II'},
                {'code': '20EC7181', 'name': 'Elective Lab', 'lab': True},
                {'code': '20EC7182', 'name': 'Project Phase I', 'lab': True},
            ],
            8: [
                {'code': '20EC8101', 'name': 'Elective IV'},
                {'code': '20EC8102', 'name': 'Elective V'},
                {'code': '20EC8181', 'name': 'Project Phase II', 'lab': True},
                {'code': '20EC8182', 'name': 'Comprehensive Viva', 'lab': True},
            ],
        },
        'EEE': {
            3: [
                {'code': '20EE3101', 'name': 'Mathematics III'},
                {'code': '20EE3102', 'name': 'Electrical Machines I'},
                {'code': '20EE3103', 'name': 'Network Analysis'},
                {'code': '20EE3104', 'name': 'Electromagnetic Fields'},
                {'code': '20EE3105', 'name': 'Analog Electronics'},
                {'code': '20EE3181', 'name': 'Electrical Machines Lab I', 'lab': True},
                {'code': '20EE3182', 'name': 'Electronics Lab', 'lab': True},
            ],
            4: [
                {'code': '20EE4101', 'name': 'Electrical Machines II'},
                {'code': '20EE4102', 'name': 'Power Systems I'},
                {'code': '20EE4103', 'name': 'Control Systems'},
                {'code': '20EE4104', 'name': 'Digital Electronics'},
                {'code': '20EE4105', 'name': 'Measurements and Instrumentation'},
                {'code': '20EE4181', 'name': 'Electrical Machines Lab II', 'lab': True},
                {'code': '20EE4182', 'name': 'Control Systems Lab', 'lab': True},
            ],
            5: [
                {'code': '20EE5101', 'name': 'Power Systems II'},
                {'code': '20EE5102', 'name': 'Power Electronics'},
                {'code': '20EE5103', 'name': 'Microprocessors'},
                {'code': '20EE5104', 'name': 'Renewable Energy Systems'},
                {'code': '20EE5105', 'name': 'Signals and Systems'},
                {'code': '20EE5181', 'name': 'Power Electronics Lab', 'lab': True},
                {'code': '20EE5182', 'name': 'Microprocessor Lab', 'lab': True},
            ],
            6: [
                {'code': '20EE6101', 'name': 'High Voltage Engineering'},
                {'code': '20EE6102', 'name': 'Switchgear and Protection'},
                {'code': '20EE6103', 'name': 'Electric Drives'},
                {'code': '20EE6104', 'name': 'Smart Grid'},
                {'code': '20EE6105', 'name': 'Industry Specific Employability Skills'},
                {'code': '20EE6181', 'name': 'Power Systems Lab', 'lab': True},
                {'code': '20EE6182', 'name': 'Drives Lab', 'lab': True},
                {'code': '20HS6101', 'name': 'Technical Paper Writing & IPR'},
                {'code': '20PT6A19', 'name': 'P & T Verbal Ability'},
                {'code': '20PT6C20', 'name': 'P & T Coding'},
            ],
            7: [
                {'code': '20EE7101', 'name': 'Elective I'},
                {'code': '20EE7102', 'name': 'Elective II'},
                {'code': '20EE7103', 'name': 'Elective III'},
                {'code': '20EE7104', 'name': 'Open Elective I'},
                {'code': '20EE7105', 'name': 'Open Elective II'},
                {'code': '20EE7181', 'name': 'Elective Lab', 'lab': True},
                {'code': '20EE7182', 'name': 'Project Phase I', 'lab': True},
            ],
            8: [
                {'code': '20EE8101', 'name': 'Elective IV'},
                {'code': '20EE8102', 'name': 'Elective V'},
                {'code': '20EE8181', 'name': 'Project Phase II', 'lab': True},
                {'code': '20EE8182', 'name': 'Comprehensive Viva', 'lab': True},
            ],
        },

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
        }
    }

    if semester <= 2:
        if semester == 1:
            return common_s1
        else:
            return common_s2
    else:
        # Return department-specific list for that semester
        return dept_subjects[dept][semester]

# ----------------------------------------------------------------------
# Helper: map semester number to year label and roman numeral
# ----------------------------------------------------------------------
sem_to_year = {1: 'I', 2: 'I', 3: 'II', 4: 'II', 5: 'III', 6: 'III', 7: 'IV', 8: 'IV'}
sem_roman = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII']

# ----------------------------------------------------------------------
room_numbers = [str(i) for i in range(1201, 1400)]

# ----------------------------------------------------------------------
# Function to assign faculty to subjects for a given section
# ----------------------------------------------------------------------
def assign_faculty(subject_list, dept, semester, section):
    """Assign a faculty from the pool based on a hash of subject code and section."""
    faculty_names = list(faculty_pool.keys())
    assigned = []
    for subj in subject_list:
        code = subj['code']
        # Combine code and section to get a deterministic index
        hash_val = (hash(code) + hash(section)) % len(faculty_names)
        faculty_name = faculty_names[hash_val]
        faculty_id = faculty_pool[faculty_name]
        subj_copy = subj.copy()
        subj_copy['faculty'] = f"{faculty_name}({faculty_id})"
        assigned.append(subj_copy)
    return assigned

# ----------------------------------------------------------------------
# Build the complete dataset for all classes
# ----------------------------------------------------------------------
all_classes = []
room_index = 0

department_branches = [
    ('AI', 'AIML', ['A', 'B']),
    ('AI', 'AIDS', ['A', 'B']),
    ('CSE', 'CSE', ['A', 'B']),
    ('IT', 'IT', ['A', 'B']),
    ('ECE', 'ECE', ['A', 'B']),
    ('EEE', 'EEE', ['A', 'B']),
    ('MECH', 'MECH', ['A', 'B']),
    ('CIVIL', 'CIVIL', ['A', 'B']),
]

for dept, branch, sections in department_branches:
    for section in sections:
        for sem in range(1, 9):
            year_label = sem_to_year[sem]
            subjects_raw = get_subjects_for_dept(branch, sem)
            subjects_with_faculty = assign_faculty(subjects_raw, dept, sem, section)

            class_sem_str = f"{year_label} {branch} - {section} / {sem_roman[sem-1]} SEM"

            room_no = room_numbers[room_index % len(room_numbers)]
            room_index += 1

            class_entry = {
                'department': dept,
                'branch': branch,
                'section': section,
                'room_no': room_no,
                'date': 'TBD',
                'academic_year': '2025-2026',
                'class_sem': class_sem_str,
                'timetable': {},
                'subjects': subjects_with_faculty,
                'abbr_to_faculty': {}
            }
            all_classes.append(class_entry)

# ----------------------------------------------------------------------
# Build abbreviation mapping for each class (simplified)
# ----------------------------------------------------------------------
def get_abbreviation(subject_name):
    name = subject_name.lower()
    if 'operating systems' in name: return 'OS'
    if 'deep learning' in name and 'lab' not in name: return 'DL'
    if 'computer networks' in name: return 'CN'
    if 'data visualization' in name and 'lab' not in name: return 'DV'
    if 'cloud computing' in name: return 'CC'
    if 'industry' in name: return 'ISES'
    if 'soft skills' in name: return 'SS'
    if 'technical paper' in name: return 'TPW'
    if 'verbal' in name: return 'PT(V)'
    if 'coding' in name: return 'PT(C)'
    if 'machine learning' in name and 'lab' not in name: return 'ML'
    if 'reinforcement learning' in name: return 'RL'
    if 'software engineering' in name and 'lab' not in name: return 'SE'
    if 'object oriented' in name: return 'OOAD'
    if 'data mining' in name: return 'DM'
    if 'big data' in name: return 'BD'
    if 'computer vision' in name: return 'CV'
    if 'natural language' in name: return 'NLP'
    if 'web technologies' in name: return 'WEB'
    if 'database' in name or 'dbms' in name: return 'DBMS'
    if 'python' in name: return 'PY'
    if 'data structures' in name: return 'DS'
    if 'algorithm' in name: return 'DAA'
    if 'probability' in name: return 'P&S'
    if 'discrete' in name: return 'DM'
    if 'mathematics' in name: return 'M'
    if 'physics' in name: return 'PHY'
    if 'chemistry' in name: return 'CHEM'
    if 'programming' in name: return 'PROG'
    if 'engineering' in name and 'graphics' in name: return 'EG'
    if 'workshop' in name: return 'WS'
    if 'environmental' in name: return 'EVS'
    if 'constitution' in name: return 'IC'
    if 'lab' in name:
        base = name.replace('lab', '').strip()
        return get_abbreviation(base) + ' LAB'
    if 'project' in name: return 'PROJ'
    if 'elective' in name: return 'ELE'
    if 'engineering mechanics' in name: return 'EM'
    if 'english' in name: return 'ENG'
    if 'electrical' in name: return 'BEE'
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
    return name[:3].upper()

for cls in all_classes:
    cls['abbr_to_faculty'] = {}
    for subj in cls['subjects']:
        abbr = get_abbreviation(subj['name'])
        cls['abbr_to_faculty'][abbr] = subj['faculty']
        # Add common variations
        if abbr == 'OS':
            cls['abbr_to_faculty']['O.S'] = subj['faculty']
        if abbr == 'SS':
            cls['abbr_to_faculty']['S.S'] = subj['faculty']
        if abbr == 'TPW':
            cls['abbr_to_faculty']['T.PW'] = subj['faculty']
        if abbr == 'PT(V)':
            cls['abbr_to_faculty']['PT(V)'] = subj['faculty']
        if abbr == 'PT(C)':
            cls['abbr_to_faculty']['PT(C)'] = subj['faculty']
        if abbr == 'CC':
            cls['abbr_to_faculty']['CC'] = subj['faculty']
        if abbr == 'DV':
            cls['abbr_to_faculty']['DV'] = subj['faculty']
        if abbr == 'CN':
            cls['abbr_to_faculty']['CN'] = subj['faculty']
        if abbr == 'ISES':
            cls['abbr_to_faculty']['ISES'] = subj['faculty']
        if abbr == 'DL':
            cls['abbr_to_faculty']['DL'] = subj['faculty']
        if abbr == 'ML':
            cls['abbr_to_faculty']['ML'] = subj['faculty']
        if abbr == 'DS':
            cls['abbr_to_faculty']['DS'] = subj['faculty']
        if abbr == 'AI':
            cls['abbr_to_faculty']['AI'] = subj['faculty']

def get_class_data(class_sem_str):
    for cls in all_classes:
        if cls['class_sem'] == class_sem_str:
            return cls
    return None

def get_faculty_timetable(faculty_name):
    schedule = {day: [[] for _ in range(8)] for day in ['MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT']}
    for cls in all_classes:
        class_name = cls['class_sem']
        tt = cls.get('timetable', {})
        if not tt:
            continue
        for day, periods in tt.items():
            for p, abbr in enumerate(periods):
                if abbr and abbr.strip():
                    faculty = cls['abbr_to_faculty'].get(abbr)
                    if faculty and faculty_name.lower() in faculty.lower():
                        schedule[day][p].append(f"{class_name}: {abbr}")
    return schedule

def get_student_timetable(class_sem_str):
    cls = get_class_data(class_sem_str)
    if cls:
        return cls.get('timetable'), cls
    return None, None

def get_required_periods(subject):
    name = subject['name'].lower()
    if 'lab' in name or 'project' in name or 'workshop' in name or 'viva' in name:
        return 3
        
    # Non-mandatory or skill-based subjects (3 times a week)
    unmandatory_keywords = [
        'skills', 'employability', 'paper writing', 'verbal', 'coding', 
        'environmental', 'constitution', 'open elective'
    ]
    if any(k in name for k in unmandatory_keywords):
        return 3

    # Core/Mandatory theory subjects (Daily -> 6 periods a week for a 6-day week)
    return 6
