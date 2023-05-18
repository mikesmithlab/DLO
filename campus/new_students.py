import pandas as pd

import sys
# setting path
sys.path.append('..')
sys.path.append('.')
from addresses import DLO_DIR


if __name__ == '__main__':
    path = DLO_DIR + '/Admissions/'
    filename='2022_admissions.xlsx'
    df = pd.read_excel(path + filename, sheet_name='Conditional Firm', na_filter=False)
    df[['First Name','Last Name','Student Id','UCAS Disability','Extenuating Circumstances Discussed', 'Needs flagged in Application','Flags in Reference']].head()
    
