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
    
    meeting_record = requests.get(f"https://graph.microsoft.com/beta/communications/callRecords/{os.environ['MEETING_ID']}", headers=headers)
    
    organizer_id = meeting_record.json()['organizer']['user']['id']
    meeting_url = meeting_record.json()['joinWebUrl']

    print(f"organizer_id :  {organizer_id}")
    print(f"meeting_url :  {meeting_url}")

    res = requests.get(f"https://graph.microsoft.com/beta/users/{organizer_id}/onlineMeetings?$filter=JoinWebUrl%20eq%20'{meeting_url}'", headers=headers)

    online_meeting_id = res.json()['value'][0]['id']
    print(f"online_meeting_id :  {online_meeting_id}")

    # Get transcript id from the meeting id
    transcript_res = requests.get(f"https://graph.microsoft.com/beta/users/{organizer_id}/onlineMeetings/{online_meeting_id}/transcripts", headers=headers)
    transcript_id = transcript_res.json()['value'][0]['id']
    print(f"transcript_id :  {transcript_id}")

    content_headers = {
        "Authorization" : f"Bearer {access_Token}",
        "Content-Type" : "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "Accept" : "application/json"      
    } 

    # Get transcript content
    transcript_content_res = requests.get(f"https://graph.microsoft.com/beta/users/{organizer_id}/onlineMeetings/{online_meeting_id}/transcripts/{transcript_id}/content?$format=text/vtt", headers=content_headers)
    
    # Convert transcript content
    decoded_response = transcript_content_res.content.decode("utf-8")
    
    # Print transcript content
    print(f"Transcript Content:")
    print(decoded_response)
