import pandas as pd
import numpy as np

filepath = 'C:\\Users\\ppzmis\\OneDrive - The University of Nottingham\\Documents\\DLO\\'
filename = 'StudentExport_ppzmis_' + '09_November_2022_1341.xlsx'


df_students = pd.read_excel(filepath+filename, sheet_name='1',skiprows=[0])
df_accomodations = pd.read_excel(filepath+filename,sheet_name='Accommodations',skiprows=[0])

filter = 'EXM'


df_exams = df_accomodations[df_accomodations['Accommodation Type'].str.contains(filter)]
student_ids = df_exams['Student ID']

levels = []
for id in student_ids:
    levels.append(df_students[df_students['Student ID'] == id]['Level'])
levels = np.array(levels)

df_exams['Level']=levels
print(df_exams['Level'].str.contains('Second'))
yr3 = df_exams[df_exams['Level'].str.contains('Third').astype(bool)]
yr2 = df_exams[df_exams['Level'].str.contains('Second').astype(bool)]



yr3.to_excel(filepath + 'yr3.xlsx', index=False)
yr2.to_excel(filepath + 'yr2.xlsx',index=False)


