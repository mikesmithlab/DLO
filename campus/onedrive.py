from email import header
import os
from re import A
from msgraph import generate_access_token, GRAPH_API_ENDPOINT
import requests
import json
import base64
from typing import List


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
    with open(local_file_path, 'rb') as upload:
        media_content = upload.read()

    response=requests.put(
        GRAPH_API_ENDPOINT + '/me/drive/items/'+onedrive_folder+f'{onedrive_file_name}:/content',
        headers=headers,
        data=media_content
    )
    return response


def create_share_link(folder_path, emails, link_type='view'):
    folder_id = get_folder_id(folder_path)   
    
    request = {
        "type": link_type,
        "scope": "organization",
        }

    response=requests.post(
        GRAPH_API_ENDPOINT + '/me/drive/items/' + folder_id + '/createLink',
        headers=headers,
        json=request
        )
    
    share_link = response.json()['link']['webUrl']
    share_id = response.json()['shareId']
    add_permission(share_id, emails)

    return share_link

def list_permission(folder_path):   
    """Lists current permissions for a particular folder path.

    Parameters
    ----------
    folder_path : str
        should look like 'root:/Documents/DLO/Campus/modules/test'

    Returns
    -------
    _type_
        _description_
    """
    response=requests.get(
        GRAPH_API_ENDPOINT + '/me/drive/items/' + folder_id + ':/permissions',
        headers=headers,
    )
    return response
    
def remove_permission(folder_path, emails : List[str]):
    """Remove permission to user to use link

    Docs - https://learn.microsoft.com/en-us/graph/api/permission-grant?view=graph-rest-1.0&tabs=http

    Parameters
    ----------
    folder_path : str
        should look like 'root:/Documents/DLO/Campus/modules/test'
    user_email : List of emails to remove permission from

    """
    recipients = [{"email":email} for email in emails]

    folder_id = get_folder_id(folder_path)

    response=requests.delete(
        GRAPH_API_ENDPOINT + '/me/drive/items/' + folder_id + '/permissions/grant',
        headers=headers,
        )

    return response 

def add_permission(share_id, emails : List[str]):
    """Grant permission to user to use link

    Docs - https://learn.microsoft.com/en-us/graph/api/permission-grant?view=graph-rest-1.0&tabs=http

    Parameters
    ----------
    share_id : An id linked to the share link
    user_email : List of emails to grant permission to
    expirationDateTime : Needs implementing in request

    """
    recipients = [{"email":email} for email in emails]

    request = {
        "recipients": recipients,
        "roles": ["read"],
        }

    response=requests.post(
        GRAPH_API_ENDPOINT + '/shares/' + share_id + '/permission/grant',
        headers=headers,
        json=request
        )

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
   
    return response.json()['id']



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

    folder_path = 'root:/Documents/DLO/Campus/modules/test'
    #get_folder_id(folder_path)
    response=list_permission(folder_path)
    print(response.json()['value'][0]['grantedToIdentitiesV2'][0]['user']['email'])#['grantedToIdentitiesV2'])#[0]['displayName'])
    #share_folder(folder_path, 'michael.swift@nottingham.ac.uk')
    link = create_share_link(folder_path,['michael.swift@nottingham.ac.uk'])
    #print(link)

