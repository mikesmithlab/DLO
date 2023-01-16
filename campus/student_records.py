

import os, sys


# setting path
parent = os.path.abspath('.')
parent2 = os.path.abspath('..')
sys.path.insert(1, parent)
sys.path.insert(1,parent2)


import pandas as pd
import numpy as np
from pprintpp import pprint

from addresses import DLO_DIR


from custom_datatypes import StudentId, YearGroup


def get_student_record(id=0,name=('',''), show=False, filepath=DLO_DIR +'Campus/',filename='student_export.xlsx'):# : StudentId=0, name=('', ''), print=False, ):
    df_students = pd.read_excel(filepath + filename, sheet_name='Students', usecols=['Student ID','Surname','First Name','Email','Level','Accommodations','Start Date','Expected End Date', 'Modules', 'Personal Tutor 1','Tutor 1 Email Address'])
    try:
        if id == 0:
            df_surname = df_students[df_students['Surname'].str.contains(name[1], case=False)]
            student = df_surname[df_surname['First Name'].str.contains(name[0], case=False)]
            id = StudentId(student['Student ID'].iloc[0])
        else:
            id = StudentId(id)
    except:
        print('Entry not found')

    student = df_students[df_students['Student ID'] == id]


    student_record = {
            'id':id,
            'first name': student['First Name'].iloc[0],
            'surname': student['Surname'].iloc[0],
            'email': student['Email'].iloc[0],
            'level': YearGroup(student['Level'].iloc[0]),
            'start date': student['Start Date'].iloc[0],
            'end date': student['Expected End Date'].iloc[0],
            'tutor': student['Personal Tutor 1'].iloc[0],
            'tutor email': student['Tutor 1 Email Address'].iloc[0]
    }

    if student['Modules'].values.any():
        student_record['modules'] = None
    else:
        modules = {module[:8]: module[8:] for module in student['Modules'].iloc[0].split(';')}
        student_record['modules'] = modules

    if student['Accommodations'].iloc[0] == 'Yes':
        df_support = pd.read_excel(filepath + filename, sheet_name='Accommodations', usecols=['Student ID','Surname','First Name','Email','Accommodation Type','Accommodation Description'])
        df_student_support = df_support[df_support['Student ID']==id]
        accommodations = {accommodation[:6]: accommodation[6:] for accommodation in df_student_support['Accommodation Type'].to_list()}
        student_record['support plan']=accommodations
    else:
        student_record['support plan'] = 'None'

    if show:
        pprint(student_record)

    return student_record






if __name__ == '__main__':

    while True:
        entry = input("Type student id or name separated by comma. q to quit>")
        if entry == 'q':
            break
        elif ',' in entry:
            name = entry.strip().split(',')
            print(name)

            get_student_record(name=(name[0],name[1]), show=True)
        else:
            get_student_record(id=entry, show=True)




