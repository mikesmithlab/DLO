
import pandas as pd

import sys
sys.path.append('..')
from addresses import DLO_DIR

def student_info(surname=None, firstname=None, student_id=None, filename='Campus/StudentExport.xlsx'):
    """find tutor info from student

    Supply either surname and firstname or student_id
    """
    df = pd.read_excel(DLO_DIR + filename, sheet_name='1',skiprows=[0])
    if surname is not None:
        student_record = df[(df['Surname'].str.lower() == surname.lower()) & (df['firstname'].str.lower() == firstname.lower())]
    elif student_id is not None:
        student_record = df[df['Student ID'] == student_id]

    student_record = student_record.squeeze()
    try:
        modules = ['PHYS' + x.split(' ')[0] for x in student_record['Courses'].str.split('PHYS')]
    except:
        modules=None

    info = {
            'student_surname':student_record['Surname'],
            'student_firstname':student_record['First Name'],
            'student_id':student_record['Student ID'],
            'modules':modules,
            'tutor':student_record['Personal Tutor 1'],
            'tutor_email':student_record['Tutor 1 Email Address'],
            'accommodations':None
        }

    #Check for accommodations in support plan
    df = pd.read_excel(DLO_DIR + filename, sheet_name='Accommodations',skiprows=[0])
    if student_id in df['Student ID'].values:
        student = df[df['Student ID']==student_id]
        accommodations= student.groupby('Student ID').apply(lambda group: ','.join(group['Accommodation Type']))
        print(accommodations)
        info['accommodations'] = [code.split(' ')[-1] + ')' for code in accommodations.split('),')]
        print(info)
    return info

def get_module_convenor_info(module_code, filename='/Campus/module_convenors.xlsx'):
    """find module convenor from module code

    Supply either surname and firstname or student_id
    """
    df = pd.read_excel(DLO_DIR + filename)
    module = df[df['Campus Code'] == module_code].squeeze()
    info = {
        'convenor':module['Convenor'],
        'convenor_email':module['emails'],
        'module_name':module['Module Title']
    }
    return info





def students_on_module():
    pass



if __name__ == '__main__':
    #get_tutor_info(student_id=14330003)
    #get_module_convenor_info('PHYS2001')
    student_info(student_id=20235034)