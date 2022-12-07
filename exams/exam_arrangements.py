import pandas as pd
import numpy as np
import glob

import sys
# setting path
sys.path.append('..')
from addresses import DLO_DIR

filepath = DLO_DIR + 'Campus/'
filename = 'StudentExport.xlsx'


df_students = pd.read_excel(filepath+filename, sheet_name='1',skiprows=[0])
df_accommodations = pd.read_excel(filepath+filename,sheet_name='Accommodations',skiprows=[0])


df_accommodations = df_accommodations[df_accommodations['Unnamed: 18'].str.contains('Active')]
df_exams = df_accommodations[df_accommodations['Accommodation Type'].str.contains('EXM')]
student_ids = df_exams['Student ID']

levels = []
for id in student_ids:
    levels.append(df_students[df_students['Student ID'] == id]['Level'])
levels = np.array(levels)

df_exams['Level']=levels



yr3 = df_exams[df_exams['Level'].str.contains('Third').astype(bool)]
yr2 = df_exams[df_exams['Level'].str.contains('Second').astype(bool)]
yr1 = df_exams[df_exams['Level'].str.contains('First').astype(bool)]

exam_accommodations=pd.DataFrame(df_accommodations['Accommodation Type'].str.contains('EXM').unique())
teach_accommodations=pd.DataFrame(df_accommodations['Accommodation Type'].str.contains('TCH').unique())
other_accommodations = pd.DataFrame(df_accommodations[df_accommodations['Accommodation Type'].str.contains('EXM|TCH')==False]['Accommodation Type'].unique())

current_accommodations =pd.concat([exam_accommodations, teach_accommodations, other_accommodations], axis=1)
current_accommodations.to_excel(filepath + '/current_accommodations.xlsx', index=False)



yr3.to_excel(filepath + '/exam_accommodations/yr3.xlsx', index=False)
yr2.to_excel(filepath + '/exam_accommodations/yr2.xlsx',index=False)
yr1.to_excel(filepath + '/exam_accommodations/yr1.xlsx',index=False)


