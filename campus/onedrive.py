import os
from re import A
from msgraph import generate_access_token, GRAPH_API_ENDPOINT
import requests


def upload_file(local_file_path, onedrive_folder, onedrive_file_name):
    """Upload a file to Onedrive

    Docs for api : https://learn.microsoft.com/en-us/onedrive/developer/rest-api/api/driveitem_put_content?view=odsp-graph-online

    Parameters
    ----------
    local_file_path : Filepath to file to be uploaded
    onedrive_folder : Where to store file in onedrive
    file_name : new name of file to be stored in onedrive   

    Returns
    -------
    response
    (https://learn.microsoft.com/en-us/onedrive/developer/rest-api/api/driveitem_put_content?view=odsp-graph-online)
    """
    with open(file_path, 'rb') as upload:
        media_content = upload.read()

    response=requests.put(
        GRAPH_API_ENDPOINT + '/me/drive/items/'+filepath+f'{file_name}:/content',
        headers=headers,
        data=media_content
    )
    return response

def share_folder(folder_path, user_email, permission='read_only'):
    """Make existing folder shared with user on Onedrive
    Docs for API https://learn.microsoft.com/en-us/onedrive/developer/rest-api/api/driveitem_put_content?view=odsp-graph-online
    folder_path = 
    
    """
    response = get_folder_id(folder_path)   
    folder_id = response.json()['id']
    print(folder_id)
    #response=requests.post()
    return response

def get_folder_id(onedrive_filepath):
    """Get the id of a folder in onedrive from its path
    
    Docs for api : https://learn.microsoft.com/en-us/onedrive/developer/rest-api/api/driveitem_get?view=odsp-graph-online
    
    Parameters
    ----------
    onedrive_filepath : filepath should look like root:/Documents/DLO
        _description_
    """
    response=requests.get(
        GRAPH_API_ENDPOINT + '/me/drive/'+onedrive_filepath,
        headers=headers,
        )
    return response


    

if __name__ == '__main__':
    
    APPLICATION_ID='a4bcc85f-0755-44e4-9d8a-116d46e8ec67'
    #Scopes must match app permissions on https://portal.azure.com/
    #App is called Python Graph API
    SCOPES = ['Files.ReadWrite']#User.Read','User.Export.All'].

    #Verify identiry
    access_token = generate_access_token(APPLICATION_ID, SCOPES)

    headers = {
        'Authorization':'Bearer ' + access_token['access_token']
    }

    share_folder('root:/Documents/DLO/Campus/modules/test')

