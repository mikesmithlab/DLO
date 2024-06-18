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


def message (name, email, modulecode, link):
    return  {
                        'to'        : email,
                        'subject'   : f'Accommodations summary for module {modulecode}',
                        'body'      : f'Dear {name}, \n\nthe shared folder below contains information specific to your module {modulecode}. \n\n' + link + '\n\n' + 'This folder provides a spreadsheet with a helpful summary of the students in your module. The first page tells you whether or not they have a support plan. The second page expands on what support needs / adjustments are included in their support plan. Codes beginning TCH affect teaching and codes beginning EXM affect assessment. A (sometimes helpful!) description of what this means is also provided.\n\n This spreadsheet is dynamically updated each week from Campus and so hopefully makes it easy for you to see and plan for the students in your module. The information is only as accurate as Campus (groan...) which means students with missing modules (of which there are quite a few) will only appear as and when they are correctly registered,  but hopefully this should improve with time and makes life a bit easier for you. \n\n I know from discussions with some module leaders that for a few modules this information is particularly useful. If this applies to your module and you are able to create a more accurate list of students please send me an excel spreadsheet with filename of your module code PHYSXXXX.xlsx and column headings: Student ID, First Name, Surname and I will regenerate this information to include your full list of students. \n\n If you have others who are involved in your module you would like this summary shared with please let me know as the permissions to this information are restricted and so the link will not work. \n\n kind regards \n\n Mike' 
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


def setup_module_permissions(module_codes):
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

    # By default this runs a test using my own module. Be careful not to spam the entire school again ;-)

    root_folder_path = 'root:/Documents/DLO/Campus/modules/'   

    df_student, df_support = campus.load_campus()   
        
    module_codes = [code for code in module_codes if code[:4] =='PHYS']
    
    for code in module_codes:
        module = mr.Module(code, df_students=df_student, df_support=df_support)
        module.get_accommodations()
        module.export_module()
        convenor = module.module_info['convenor_name'][0]
        convenor_email = module.module_info['convenor_email'][0]
        
        folder_path=root_folder_path + code
        headers = onedrive.session_login()
        
        link = onedrive.create_share_link(folder_path,[convenor_email], headers)
        send_email(message(convenor, convenor_email, code, link))


if __name__ == '__main__':
    create_module_summaries()
    #module_codes = ['PHYS1002']
    #setup_module_permissions(module_codes)
   