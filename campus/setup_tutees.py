import os, sys
# setting path
parent = os.path.abspath('.')
parent2 = os.path.abspath('..')
sys.path.insert(1, parent)
sys.path.insert(1,parent2)
from addresses import DLO_DIR

import onedrive
import mynottingham as campus
import module_records as mr
import student_records as sr
from emails.auto_email import send_email
import pandas as pd


def message (tutor, email, modulecode, link):
    return  {
                        'to'        : email,
                        'subject'   : f'Accommodations summary for module {modulecode}',
                        'body'      : f'Dear {tutor}, \n\nthe shared folder below contains information specific to your tutor group. \n\n' + link + '\n\n' + 'This folder contains two spreadsheets. \n\nThe first spreadsheet lists the modules and associated points of each tutee as currently held on campus. Please check these with your tutees and let Ben McKirgan know if they are inaccurate (ben.mckirgan@nottingham.ac.uk). \n\n The second spreadsheet contains a helpful summary of the students in your tutor group. It summarises the support plan needs both in teaching and assessment. Please note this information is updated regularly with changes to campus and additional notes.\n\nIf through your engagement with them, you believe your tutees might have needs not covered by the support plan info recorded then please raise this with Mike Smith (DLO) and / or Frazer Pearce (Senior Tutor)\n\n We have also included a quick guide to the support available for your tutees, with links to the key contacts and info. \n\n kind regards\n\nMike Smith'
                    }

def modules_check():
    """Pulls the info currently on campus and a file listing which students are in which tutor groups
    generated by the school. It then pulls out the modules and does a quick check of the points. It then saves it
    in a shared folder for each tutor"""

    df_students, df_support = campus.load_campus()
    
    tutor_groups = pd.read_excel(DLO_DIR + 'Campus/source_files/Tutor_List.xlsx').groupby('Tutor 2223')
    df_modules = pd.read_excel(DLO_DIR + 'Campus/source_files/module_convenors.xlsx', usecols = ['Campus Code', 'Credits'])
    module_credits = dict(zip(df_modules['Campus Code'].tolist(), df_modules['Credits'].tolist()))

    for tutor_group in tutor_groups:
        tutees = tutor_group[1]['Student Id'].tolist()
        modules_check = pd.DataFrame(index=tutees, columns=['First Name','Surname','Modules','Credits'])
        for tutee in tutees:
            tutee_module_credits = []
            student = sr.Student(id=tutee, df_students=df_students, df_support=df_support)
            if student.student is None:
                #Student not listed on campus
                modules_check.loc[tutee,:] = ['Not Listed','Not Listed',' ',' ']
                #no_modules_or_not_listed.loc[tutee, :] = ['First Name','Surname','Modules','Credits']
            else:
                if student.modules is None:
                    #No modules listed
                    total_credits = None
                    print('No modules listed')
                else:
                    for module in student.modules:
                        try:
                            credits = module_credits[module]
                        except:
                            #Non physics modules - assume credits = 10
                            credits = 10                
                        tutee_module_credits.append(credits)

                    total_credits = sum(tutee_module_credits)
                modules_check.loc[tutee,:] = [student.record['first name'],student.record['surname'],student.modules,total_credits]
        tutor_group_folder = DLO_DIR + 'Campus/tutor_groups/' + tutor_group[0]
        if not os.path.exists(tutor_group_folder):
            os.mkdir(tutor_group_folder)
        modules_check.to_excel(tutor_group_folder + '/modules_check.xlsx')

def setup_tutor_permissions():
     """Setup OAUTH2 protocol login"""
    #APPLICATION_ID='a4bcc85f-0755-44e4-9d8a-116d46e8ec67'
    #Scopes must match app permissions on https://portal.azure.com/
    #App is called Python Graph API
    #SCOPES = ['Files.ReadWrite']#User.Read','User.Export.All'].

    #Verify identiry
    #access_token = onedrive.generate_access_token(APPLICATION_ID, SCOPES)

    #headers = {
    #    'Authorization':'Bearer ' + access_token['access_token']
    #}
    print('not implemented yet')

if __name__ == '__main__':
    
   
  
    modules_check()
    setup_module_permissions()