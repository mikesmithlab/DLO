

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
from custom_exceptions import AccommodationsFilterException






class Module:
    def __init__(self, module_id, df_students=None, df_support=None):
        """Extract all students associated with a module"""
        self.module = df_students[df_students['Modules'].str.contains(module_id, case=False).fillna(False, inplace=False)]
        self.student_info = { 'id' :self.module['Student ID'].tolist()}
        self.num_students = np.shape(self.module)[0]
        self.module_id = module_id
        self.module_support=df_support[df_support['Student ID'].isin(self.student_info['id'])]
        self.get_module_info()
        self.get_student_info()
        self.get_accommodations()
        
    def get_module_info(self, module_convenors_file = DLO_DIR + 'Campus/module_convenors.xlsx'):
        convenors = pd.read_excel(module_convenors_file)
        
        module = convenors[convenors['Campus Code']==self.module_id]

        self.module_info = {'convenor':module['Convenor'].values[0],
                            'convenor_email': module['emails'].values[0],
                            'module_id':self.module_id,
                            'module_title':module['Module Title'].values[0],
                            'num_students':self.num_students}
    
    def get_student_info(self):
        self.student_info['First Name'] = self.module['First Name'].tolist()
        self.student_info['Surname'] = self.module['Surname'].tolist()
        self.student_info['Accommodations'] = self.module['Accommodations'].to_list()
    
    def get_accommodations(self, filter='all'):
        """returns a dictionary of all adjustment codes and a list of student ids with that adjustment
        
        the adjustments can be filtered to include
        'all', 'exam', 'teaching' 

        'teaching' includes both assessment and teaching adjustments - ie things module convenors need to know about. These are codes beginning ASS or TCH
        'exam' includes exam adjustments. Codes beginning EXM

        """
        self.support_info = get_support(self.module_support, filter=filter)
    
    def export_module(self):
        pd.DataFrame(self.student_info).to_excel(DLO_DIR + 'Campus/modules/' + self.module_id +'_studentinfo.xlsx', index=False)
        pd.Series(self.module_info).to_excel(DLO_DIR + 'Campus/modules/' + self.module_id +'_moduleinfo.xlsx', header=False)
        pd.Series(self.support_info).to_excel(DLO_DIR + 'Campus/modules/' + self.module_id +'_supportinfo.xlsx', header=False)


class Student:

    def __init__(self, id=0, name=('',''), df_students=None, df_support=None):
        """Extract complete student record from downloaded version of campus   

        Supply either student id or name in format firstname,lastname. The firstname and lastname can be substrings
        which are contained in the name. If more than one student matches it returns possible matches

        A student has:
        1. a record --> Info such as tutor, dates, year stored as dictionary
        2. a list of modules --> Dictionary of Key, Values = Module code, Module description
        3. support --> This is None if no support plan or a dictionary of the adjustments for that student
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

    def print_student(self):
        print('-----Student Details-----')
        pprint(self.record)
        print('-----Modules-----')
        pprint(self.modules)
        print('-----Accommodations-----')
        pprint(self.support)
    
    def export_student(self):
        pd.DataFrame(self.record).to_excel(DLO_DIR + 'students/' + self.record['first name']+self.record['surname']+'_'+self.record['id']+'.xlsx')


def get_support(df_support, filter='all'):
    """get_support filters a dataframe by accommodations and returns a unique list of accommodation codes
    
        df_support a pandas dataframe containing a subset of the campus accommodations tab
        filter - can be 'all','exam', 'teaching'
        
        'teaching' includes both assessment and teaching adjustments - ie things module convenors need to know about. These are codes beginning ASS or TCH
        'exam' includes exam adjustments. Codes beginning EXM
        'all' returns everything
    """
    if filter == 'exam':
        df = df_support[df_support['Accommodation Type'].str.contains('EXM')]
    elif filter == 'teaching':
        df = df_support[df_support['Accommodation Type'].str.contains('TCH | ASS')]
    elif filter == 'all':
        df=df_support
    else:
        raise AccommodationsFilterException
    
    codes = df.groupby('Accommodation Type')    
    unique_codes = [code[:6] for code in codes.groups.keys()]
    count_students = [len(value) for value in codes.groups.values()]
    support = {code : count for code, count in zip(unique_codes, count_students)}
       
    return support
    

def load_campus(filepath=DLO_DIR +'Campus/', filename='student_export.xlsx'):
    """Loads the contents of the Campus download file into two dataframes
    1. The students tab
    2. The accommodations tab
    """
    df_students = pd.read_excel(filepath + filename, sheet_name='Students', usecols=['Student ID','Surname','First Name','Email','Level','Accommodations','Start Date','Expected End Date', 'Modules', 'Personal Tutor 1','Tutor 1 Email Address'])
    df_support = pd.read_excel(filepath + filename, sheet_name='Accommodations', usecols=['Student ID','Surname','First Name','Email','Accommodation Type','Accommodation Description'])
    return df_students, df_support


if __name__ == '__main__':
    df_student, df_support = load_campus()
    
    #fnf = Module('PHYS3009', df_students=df_student, df_support=df_support)
    #fnf.export_module()
    
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
        student.print_student()

    

