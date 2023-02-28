

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


from custom_datatypes import StudentId, YearGroup, ModuleCode

class Module:
    def __init__(self, module_id, df_students=None, df_support=None):
        """Extract all students associated with a module"""
        self.module = df_students[df_students['Modules'].str.contains(module_id, case=False).fillna(False, inplace=False)]
        self.num_students=np.shape(self.module)[0]
        self.get_student_ids()
        self.module_support=df_support[df_support['Student ID'].isin(self.student_info['id'])]
        self.get_students()
        
    def get_student_ids(self):
        self.student_info = { 'id' :self.module['Student ID'].tolist()}

    
    def get_students(self):
        self.students = []
        for id in self.student_info['id']:
            self.students.append(Student(id=id, df_students=self.module, df_support=self.module_support))
        
        self.student_info['First Name'] = self.module['First Name'].tolist()
        self.student_info['Surname'] = self.module['Surname'].tolist()
        
            
    
    

        



class Student:
    def __init__(self, id=0, name=('',''), df_students=None, df_support=None):
        """Extract complete student record from downloaded version of campus   

        Supply either student id or name in format firstname,lastname. The firstname and lastname can be substrings
        which are contained in the name. 
        """
        self.student=self._get_student(df_students, id=id, name=name)

        self.record=None
        self.modules=None
        self.support=None

        if self.student is not None:
            self.record=self._get_student_record()
            self.modules=self._get_student_modules()
            self.support=self._get_student_accommodations(df_support)
        

    def _get_student(self, df_students, id=0, name=(" "," ")):
        #If name given check for matches. Either return record or possible names that match.
        #Entry from database stored in self.student
        if id==0:
            df_surname = df_students[df_students['Surname'].str.contains(name[1].replace(' ',''), case=False)]
            students = df_surname[df_surname['First Name'].str.contains(name[0].replace(' ',''), case=False)]
        else:
            students = df_students[df_students['Student ID'] == id]
        
        if students.empty:
            print('No entries found')
            return None
        elif np.shape(students)[0] > 1:
            print('Multiple entries match:\n')
            for id, firstname, surname in zip(students['Student ID'].to_list(), students['First Name'].to_list(),students['Surname'].to_list()):
                print(id, firstname, surname)
            return None
        else:
            return students
        
    def _get_student_record(self):
        
        record = {
            'id':self.student['Student ID'].iloc[0],
            'first name': self.student['First Name'].iloc[0],
            'surname': self.student['Surname'].iloc[0],
            'email': self.student['Email'].iloc[0],
            'level': YearGroup(self.student['Level'].iloc[0]),
            'start date': self.student['Start Date'].iloc[0],
            'end date': self.student['Expected End Date'].iloc[0],
            'tutor': self.student['Personal Tutor 1'].iloc[0],
            'tutor email': self.student['Tutor 1 Email Address'].iloc[0]
            }
        return record
        
    def _get_student_modules(self):
        if self.student['Modules'].isna().any():
            modules = None
        else:
            modules = {module.replace(' ','')[:8]: module.replace(' ','')[8:] for module in self.student['Modules'].iloc[0].split(';')}
        return modules
            
    def _get_student_accommodations(self, df_support):
        support=None
        if self.student['Accommodations'].iloc[0] == 'Yes':   
            df_student_support = df_support[df_support['Student ID']==self.student['Student ID'].iloc[0]]
            support = {accommodation.replace(' ','')[:6]: accommodation.replace(' ','')[6:] for accommodation in df_student_support['Accommodation Type'].to_list()}
        return support

    def print_student_record(self):
        print('-----Student Details-----')
        pprint(self.record)
        print('-----Modules-----')
        pprint(self.modules)
        print('-----Accommodations-----')
        pprint(self.support)


def load_campus(filepath=DLO_DIR +'Campus/', filename='student_export.xlsx'):
    
    df_students = pd.read_excel(filepath + filename, sheet_name='Students', usecols=['Student ID','Surname','First Name','Email','Level','Accommodations','Start Date','Expected End Date', 'Modules', 'Personal Tutor 1','Tutor 1 Email Address'])
    df_support = pd.read_excel(filepath + filename, sheet_name='Accommodations', usecols=['Student ID','Surname','First Name','Email','Accommodation Type','Accommodation Description'])
    return df_students, df_support


if __name__ == '__main__':
    df_student, df_support = load_campus()
    
    fnf = Module('PHYS3009', df_students=df_student, df_support=df_support)
    """
    while True:
        entry = input("Type student id or name separated by comma. q to quit>")
        if entry == 'q':
            break
        elif ',' in entry:
            name = entry.split(',')
            print(name)
            student=Student(name=(name[0],name[1]), df_students=df_student, df_support=df_support)
        else:
            student=Student(id=entry, df_students=df_student, df_support=df_support)
        student.print_student_record()

    """

