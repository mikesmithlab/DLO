from lib2to3.pytree import convert
from pickletools import string1
import pandas as pd
import numpy as np
import glob

import os, sys
# setting path
parent = os.path.abspath('.')
sys.path.insert(1, parent)
from addresses import DLO_DIR


def get_unique_codes(df, filepath=DLO_DIR +'Campus/', output_filename='accommodation_codes.xlsx', ):
    accommodation_codes = df['Accommodation Type'].str.split(pat=' - ', n=0,expand=True)
    accommodation_codes=accommodation_codes.drop_duplicates()
    accommodation_codes = accommodation_codes[[0,1]]
    accommodation_codes[0]=accommodation_codes[0].astype(str)
    accommodation_codes['Descriptions'] = df['Accommodation Description']
    accommodation_codes.sort_values(0)
    accommodation_codes.to_excel(filepath + output_filename, index=False, header=['Code', 'Explanations', 'Descriptions'])

def get_unique_modules(filepath=DLO_DIR +'Campus/',filename='student_export.xlsx'):
    """Extract all the unique module codes from the complete campus download"""
    df_students = pd.read_excel(filepath + filename, header=0)
    modules=df_students['Modules'].str.split(pat=';', n=0,expand=True)
    num_columns = np.shape(modules)[1]

    codes = modules[0].str.strip()
    codes=codes.str[:8]
    for col in range(1,num_columns):
        temp=modules[col].str.strip()
        codes = codes.append(temp.str[:8],ignore_index=True)
    codes.dropna(inplace=True)
    codes = codes.unique().tolist()
    print(codes)
    return codes




def cf_with_examples(filepath=DLO_DIR +'Campus/', filename='accommodation_codes.xlsx',examples_filename='Full list of Campus Accommodation Codes with Descriptions Dec 22.xlsx'):
    df_accommodations = pd.read_excel(filepath + filename, converters={'Code':str, 'Explanations':str, 'Descriptions':str})
    df_explanations = pd.read_excel(filepath + examples_filename, header=1, usecols=['Code','Examples'], converters={'Code':str, 'Examples':str})
    df_accommodations=df_accommodations.merge(df_explanations, on='Code', how='left', sort=True)
    df_accommodations.to_excel(filepath + filename, index=False)


def read_campus(filepath=DLO_DIR +'Campus/', filename='student_export.xlsx'):
    df_students = pd.read_excel(filepath+filename, sheet_name='Students')#,skiprows=[0])
    print(df_students['Level'].head(n=20))
    df_accommodations = pd.read_excel(filepath+filename,sheet_name='Accommodations')#,skiprows=[0])
    df_accommodations = df_accommodations[df_accommodations['Programme Status'].str.contains('Active')]
    get_unique_codes(df_accommodations)




if __name__ == '__main__':
    read_campus()
    #get_unique_modules()



