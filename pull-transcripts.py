import requests
import os

if __name__ == "__main__":

    authbody = {
        "client_id" : os.environ['CLIENT_ID'],
        "client_secret" : os.environ['CLIENT_SECRET'],
        "grant_type" : "client_credentials",
        "scope": "https://graph.microsoft.com/.default"
    }

    auth_Response = requests.post(f"https://login.microsoftonline.com/{os.environ['TENANT_ID']}/oauth2/v2.0/token", data= authbody)

    access_Token = auth_Response.json()['access_token']

    headers = {
        "Authorization" : f"Bearer {access_Token}",
        "Content-Type" : "application/json",
        "Accept" : "application/json"      
    }  

    res = requests.get(f"https://graph.microsoft.com/beta/users/{os.environ['USER_ID']}/onlineMeetings?$filter=JoinWebUrl%20eq%20'{os.environ['MEETING_URL']}'", headers=headers)
    onl_meet_data = res.json()['value'][0]['id']

    trans_res = requests.get(f"https://graph.microsoft.com/beta/users/{os.environ['USER_ID']}/onlineMeetings/{onl_meet_data}/transcripts", headers=headers)
    trans_res_data = trans_res.json()['value']

    print(onl_meet_data)
