import pandas as pd
import numpy as np
import glob

import os, sys
# setting path
parent = os.path.abspath('.')
sys.path.insert(1, parent)
from addresses import DLO_DIR


def get_unique_codes(df, filepath=DLO_DIR +'Campus/', filename='accommodation_codes.xlsx'):
    accommodation_codes = df['Accommodation Type'].str.split(pat=' - ', n=0,expand=True)
    accommodation_codes=accommodation_codes.drop_duplicates()
    accommodation_codes = accommodation_codes[[0,1]]

    accommodation_codes.to_excel(filepath + filename, index=False, header=['Codes', 'Explanations'])    


def read_campus(filepath=DLO_DIR +'Campus/', filename='student_export.xlsx'):
    df_students = pd.read_excel(filepath+filename, sheet_name='Students')#,skiprows=[0])
    df_accommodations = pd.read_excel(filepath+filename,sheet_name='Accommodations')#,skiprows=[0])
    df_accommodations = df_accommodations[df_accommodations['Programme Status'].str.contains('Active')]
    get_unique_codes(df_accommodations)








if __name__ == '__main__':
    read_campus()