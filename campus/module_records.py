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
from mynottingham import load_campus
from student_records import get_support, Student


class Module:
    def __init__(self, module_id, df_students=None, df_support=None):
        """Extract all students associated with a module"""
        self.module = df_students[df_students['Modules'].str.contains(module_id, case=False).fillna(False, inplace=False)]
        self.student_info = { 'id' :self.module['Student ID'].tolist()}
        self.num_students = np.shape(self.module)[0]
        self.module_id = module_id
        self.module_support=df_support[df_support['Student ID'].isin(self.student_info['id'])][['Student ID', 'Surname','First Name','Email','Accommodation Type']]        
        self.get_module_info()
        self.get_student_info()
        if ~self.module_support.empty:
            self.get_accommodations()
        
    def get_module_info(self, module_convenors_file = DLO_DIR + 'Campus/source_files/2324/convenors_2324.xlsx'):
        convenors = pd.read_excel(module_convenors_file)
        module = convenors[convenors['Campus Code']==self.module_id]
        self.module_info = {'convenor':module['Convenor'].values,
                            'convenor_email': module['Email'].values,
                            'convenor_name': module['Name'].values,
                            'module_id':self.module_id,
                            'module_title':module['Module Title'].values,
                            'num_students':self.num_students}
    
    def get_student_info(self):
        self.student_info['First Name'] = self.module['First Name'].tolist()
        self.student_info['Surname'] = self.module['Surname'].tolist()
        self.student_info['Accommodations'] = self.module['Accommodations'].to_list()
        
    
    def get_accommodations(self, filter='all', meaning=DLO_DIR + 'campus/source_files/campus_accommodation_codes_with_descriptions.xlsx'):
        """returns a dataframe of all adjustment codes and a list of student ids with an explanation of adjustment.
        
        the adjustments can be filtered to include
        'all', 'exam', 'teaching' 

        'teaching' includes both assessment and teaching adjustments - ie things module convenors need to know about. These are codes beginning ASS or TCH
        'exam' includes exam adjustments. Codes beginning EXM

        """
        if self.module_support.empty:
            print(f'No students with support plans in module {self.module_id}')
            return None
        else:
            explanations = pd.read_excel(meaning, header=1, usecols=['Code','Long Description','Examples'])
            
            if filter == 'exam':
                self.module_support = self.module_support[self.module_support.str.contains('EXM')]
            elif filter == 'teaching':
                self.module_support = self.module_support[self.module_support.str.contains('TCH')]
            
            temp = self.module_support['Accommodation Type'].str.split(' -',expand=True)
            explanations = explanations.set_index('Code')
            self.module_support['Code']=temp[0]
            self.module_support=self.module_support.set_index('Code')
         
            self.module_support=self.module_support.merge(explanations, left_index=True,right_index=True, how='left')
            
            if 'Examples_x' in self.module_support.columns:
                self.module_support['Examples'] = self.module_support['Examples_x']
                self.module_support['Long Description'] = self.module_support['Long Description_x']
                self.module_support.pop('Examples_x')
                self.module_support.pop('Long Description_x')
                self.module_support.pop('Examples_y')
                self.module_support.pop('Long Description_y')
            
            self.module_support = self.module_support.sort_values(['Surname','First Name'])
            return self.module_support
    
    def export_module(self):
        module_folder = DLO_DIR + 'Campus/modules/'+self.module_id
        if not os.path.exists(module_folder):
            os.mkdir(module_folder)
        with pd.ExcelWriter(module_folder + '/' + self.module_id + '_accommodations.xlsx', engine='openpyxl') as writer:
            pd.DataFrame(self.student_info).to_excel(writer, sheet_name='students', index=False)
            self.module_support.to_excel(writer, sheet_name='accommodations')

def get_unique_modules(filepath=DLO_DIR +'Campus/',filename='student_export.xlsx'):
    """Extract all the unique module codes from the complete campus download"""
    df_students = pd.read_excel(filepath + filename, header=0)
    modules=df_students['Modules'].str.split(pat=';', n=0,expand=True)
    num_columns = np.shape(modules)[1]

    codes = modules[0].str.strip()
    codes=codes.str[:8]
    for col in range(1,num_columns):
        temp=modules[col].str.strip()
        codes = pd.concat([codes,temp.str[:8]],ignore_index=True)
    codes.dropna(inplace=True)
    codes = codes.unique().tolist()
    return codes




