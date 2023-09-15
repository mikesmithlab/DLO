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
from emails.auto_email import send_email


def message (convenor, email, modulecode, link):
    return  {
                        'to'        : email,
                        'subject'   : f'Accommodations summary for module {modulecode}',
                        'body'      : f'Dear {convenor}, \n\nthe shared folder below contains information specific to your module {modulecode}. \n\n' + link + '\n\n' + 'This folder provides a spreadsheet with a helpful summary of the students in your module. It summarises the support plan needs both in teaching and assessment. They and we would appreciate it if you could ensure that you think through how to ensure your module is accessible to them. Please note this information is updated regularly with changes to campus and additional notes.\n\nIf you believe students you engage with might have needs not covered by the support plan info recorded then please let Mike Smith (DLO) or Frazer Pearce (Senior Tutor) know by...\n\n kind regards\n\nMike Smith'
                    }

def create_module_summaries():
    """Creates excel files in correct module folders summarising the support plan
    needs for students"""
    root_folder_path = 'root:/Documents/DLO/Campus/modules/'   

    df_student, df_support = campus.load_campus()
    
    module_codes = mr.get_unique_modules()#Better if this was drawn from up to date spreadsheet
    module_codes = [code for code in module_codes if code[:4] =='PHYS']

    for code in module_codes:
        module = mr.Module(code, df_students=df_student, df_support=df_support)
        module.get_accommodations()
        module.export_module()


def setup_module_permissions(test=True):
    """Setup OAUTH2 protocol login"""
    #APPLICATION_ID='API_KEY'
    #Scopes must match app permissions on https://portal.azure.com/
    #App is called Python Graph API
    #SCOPES = ['Files.ReadWrite']#User.Read','User.Export.All'].

    #Verify identiry
    #access_token = onedrive.generate_access_token(APPLICATION_ID, SCOPES)

    #headers = {
    #    'Authorization':'Bearer ' + access_token['access_token']
    #}

    # By defaul this runs a test using my own module. Be careful not to spam the entire school again ;-)

    root_folder_path = 'root:/Documents/DLO/Campus/modules/'   

    df_student, df_support = campus.load_campus()
    
    if test:
        #temp
        module_codes = ['PHYS3009']
    else:
        module_codes = mr.get_unique_modules()#Better if this was drawn from up to date spreadsheet
        module_codes = [code for code in module_codes if code[:4] =='PHYS']

    for code in module_codes:
        module = mr.Module(code, df_students=df_student, df_support=df_support)
        module.get_accommodations()
        module.export_module()
        convenor = module.module_info['convenor']
        convenor_email = module.module_info['convenor_email']
        folder_path=root_folder_path + code + '/'

        if not test:
            #onedrive.share_folder(folder_path, convenor_email)
            #link = onedrive.create_share_link(folder_path,[convenor_email])
            #send_email(message(convenor, convenor_email, code, link))

if __name__ == '__main__':
    onedrive.session_login()
    create_module_summaries()
    #setup_module_permissions()