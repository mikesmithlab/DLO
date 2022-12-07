import docx
import pandas as pd
import numpy as np

import sys
sys.path.append('..')
from addresses import DLO_DIR

def get_table_data(table, headings):
    data = pd.DataFrame(columns=headings)
    for j, row in enumerate(table.rows):
        if j!=0:
            request={}
            for i, cell in enumerate(table.row_cells(j)):
                request[headings[i]] = cell.text
            course = pd.DataFrame(request, index=[j])
            data = pd.concat([data, course])
    return data



if __name__=='__main__':
    headings=['Campus Code', 'Module Title', 'Credits', 'Convenor', 'Co-examiner','Module Team']
    doc = docx.Document(DLO_DIR + 'Teaching_Duties_By_Role_2022_2023.docx')

    df = pd.DataFrame(columns=headings)

    for table in doc.tables:
       df = pd.concat((df,get_table_data(table, headings)))

    get_emails(df)

    df.to_excel(DLO_DIR + '/Campus/module_convenors.xlsx', index=False)
