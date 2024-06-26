import webbrowser
from datetime import datetime
import json
import os
import msal

"""Module to handle log in.

Need to setup an app on Azure (https://portal.azure.com/).
Login uni username and passwd.
Check scopes match app permissions.
These youtube videos helped me understand what was going on!:
https://www.youtube.com/watch?v=1Jyd7SA-0kI&t=1s --> Method 2
https://www.youtube.com/watch?v=Ok8O_QnrSBI.

I am using the session token login which is Method 2.

This made it understandable.

"""

GRAPH_API_ENDPOINT = 'https://graph.microsoft.com/v1.0'

def generate_access_token(app_id, scopes):
    # Save Session Token as a token file
    access_token_cache = msal.SerializableTokenCache()

    # read the token file
    if os.path.exists('ms_graph_api_token.json'):
        access_token_cache.deserialize(open("ms_graph_api_token.json", "r").read())
        token_detail = json.load(open('ms_graph_api_token.json',))
        token_detail_key = list(token_detail['AccessToken'].keys())[0]
        token_expiration = datetime.fromtimestamp(int(token_detail['AccessToken'][token_detail_key]['expires_on']))
        if datetime.now() > token_expiration:
            os.remove('ms_graph_api_token.json')
            access_token_cache = msal.SerializableTokenCache()

    # assign a SerializableTokenCache object to the client instance
    client = msal.PublicClientApplication(client_id=app_id, token_cache=access_token_cache)

    accounts = client.get_accounts()
    if accounts:
        # load the session
        token_response = client.acquire_token_silent(scopes, accounts[0])
    else:
        # authenticate your account as usual
        flow = client.initiate_device_flow(scopes=scopes)
        
        # This prints a code in the terminal which you copy to the browser.
        print('user_code: ' + flow['user_code'])
        webbrowser.open('https://microsoft.com/devicelogin')
        token_response = client.acquire_token_by_device_flow(flow)

    with open('ms_graph_api_token.json', 'w') as _f:
        _f.write(access_token_cache.serialize())

    return token_response



