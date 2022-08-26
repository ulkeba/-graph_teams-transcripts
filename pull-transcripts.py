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

    # Get meeting id from the meeting url
    res = requests.get(f"https://graph.microsoft.com/beta/users/{os.environ['USER_ID']}/onlineMeetings?$filter=JoinWebUrl%20eq%20'{os.environ['MEETING_URL']}'", headers=headers)
    online_meeting_id = res.json()['value'][0]['id']

    # Get transcript id from the meeting id
    transcript_res = requests.get(f"https://graph.microsoft.com/beta/users/{os.environ['USER_ID']}/onlineMeetings/{online_meeting_id}/transcripts", headers=headers)
    transcript_id = transcript_res.json()['value'][0]['id']

    content_headers = {
        "Authorization" : f"Bearer {access_Token}",
        "Content-Type" : "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "Accept" : "application/json"      
    } 

    # Get transcript content
    transcript_content_res = requests.get(f"https://graph.microsoft.com/beta/users/{os.environ['USER_ID']}/onlineMeetings/{online_meeting_id}/transcripts/{transcript_id}/content?$format=text/vtt", headers=content_headers)
    
    # Convert transcript content
    decoded_response = transcript_content_res.content.decode("utf-8")
    
    # Print transcript content
    print(decoded_response)
