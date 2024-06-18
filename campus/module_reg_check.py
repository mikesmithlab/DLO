
import os, sys
# setting path
parent = os.path.abspath('.')
parent2 = os.path.abspath('..')
sys.path.insert(1, parent)
sys.path.insert(1,parent2)

import pandas as pd
from addresses import DLO_DIR
import student_records as sr
import mynottingham as campus

def check_module_credits(student):
    df_modules = pd.read_excel(DLO_DIR + 'Campus/source_files/2324/convenors_2324.xlsx', usecols = ['Campus Code', 'Credits'])
    credits=0
    if len(student.modules) < 2:
        if student.modules == {'':''}:
            return 0
        
    for module in student.modules:
        try:
            credits += df_modules[df_modules['Campus Code']==module]['Credits'].values[0]
        except:
            #Non physics modules - assume credits = 10
            credits += 10              
    return credits

def check_student_modules():
    df_students, df_support = campus.load_campus()
    df_credits = pd.DataFrame(columns=['First Name','Surname','Level','Personal Tutor 1','Tutor 1 Email Address','Credits','Modules'], index=df_students['Student ID'].tolist())

    for student_id in df_students['Student ID'].tolist():
        student = sr.Student(id=student_id, df_students=df_students, df_support=df_support)
        credits = check_module_credits(student)
        df_credits.loc[student_id,:] = [student.record['first name'],student.record['surname'],student.record['level'],student.record['tutor'],student.record['tutor email'],credits, student.modules]
    df_credits.to_excel(DLO_DIR + 'Campus/source_files/2324/student_credits.xlsx')


if __name__ == '__main__':
    check_student_modules()