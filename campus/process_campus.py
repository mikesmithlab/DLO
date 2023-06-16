from lib2to3.pytree import convert
from pickletools import string1
import pandas as pd
import numpy as np
import glob

import os, sys
# setting path
parent = os.path.abspath('.')
sys.path.insert(1, parent)
parent = os.path.abspath('..')
sys.path.insert(1, parent)

from addresses import DLO_DIR


def do_module_check(student_id):
    student = Student(student_id)
    student.modules



def get_unique_accommodation_codes(filepath=DLO_DIR +'Campus/', filename='student_export.xlsx', codes_filename='Full list of Campus Accommodation Codes with Descriptions Dec 22.xlsx',output_filename='accommodation_codes.xlsx'):
    """
    Create a new file of the accommodation codes present in campus and combine with descriptors
    """
    df_accommodations = pd.read_excel(filepath+filename, sheet_name='Accommodations')
    df_accommodations = df_accommodations[df_accommodations['Programme Status'].str.contains('Active')]
    df_codesexplained =pd.read_excel(filepath+codes_filename, header=1)

    accommodation_codes = df_accommodations['Accommodation Type'].str.split(pat=' - ', n=0,expand=True)
    accommodation_codes=accommodation_codes.drop_duplicates()
    accommodation_codes = accommodation_codes[[0,1]]
    accommodation_codes[0]=accommodation_codes[0].astype(str)

    df_combined = pd.merge(accommodation_codes, df_codesexplained, how='left')
    print(df_combined)
    print(np.shape(accommodation_codes))
    print(np.shape(df_combined))

    accommodation_codes['Descriptions'] = df_accommodations['Accommodation Description']
    accommodation_codes.sort_values(0)
    accommodation_codes.to_excel(filepath + output_filename, index=False, header=['Code', 'Explanations', 'Descriptions'])


def module_students(module_code, filepath=DLO_DIR +'Campus/', filename='student_export.xlsx'):
    """
    Calculate a summary of the support plan accommodations in a module
    The file contains a tab summarising module accommodations
    """
    df_students = pd.read_excel(filepath+filename, sheet_name='Students')
    df_students=df_students.dropna(subset=['Modules'])
    df_students_module = df_students[df_students['Modules'].str.contains(module_code, case=False)]

    student_ids_support = df_students_module[df_students_module['Accommodations']=='Yes']['Student ID'].to_list()
    df_accommodations = pd.read_excel(filepath+filename, sheet_name='Accommodations')
    df_module_accommodations = df_accommodations[df_accommodations['Student ID'].isin(student_ids_support)]
    split_accommodations = df_module_accommodations['Accommodation Type'].str.split(pat = ' - ',expand=True)
    df_module_accommodations['Accommodation Code']= split_accommodations[0]
    df_module_accommodations['Accommodation Type'] = split_accommodations[1]

    with pd.ExcelWriter(filepath + 'modules/' + module_code + '.xlsx', engine='openpyxl') as writer:
        df_students_module.to_excel(writer, sheet_name='students', columns=['Student ID','Surname','First Name','Title','Email','Accommodations','Personal Tutor 1','Tutor 1 Email Address'],index=False)    
        df_module_accommodations.to_excel(writer, sheet_name='accommodations', columns=['Student ID','Surname','First Name', 'Email', 'Accommodation Code','Accommodation Type','Accommodation Description'],index=False)



def cf_with_examples(filepath=DLO_DIR +'Campus/', filename='accommodation_codes.xlsx',examples_filename='Full list of Campus Accommodation Codes with Descriptions Dec 22.xlsx'):
    df_accommodations = pd.read_excel(filepath + filename, converters={'Code':str, 'Explanations':str, 'Descriptions':str})
    df_explanations = pd.read_excel(filepath + examples_filename, header=1, usecols=['Code','Examples'], converters={'Code':str, 'Examples':str})
    df_accommodations=df_accommodations.merge(df_explanations, on='Code', how='left', sort=True)
    df_accommodations.to_excel(filepath + filename, index=False)










