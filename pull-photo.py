import requests
import os
from PIL import Image
from io import BytesIO

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

    # Get photo value for user
    res = requests.get(f"https://graph.microsoft.com/v1.0//users/{os.environ['USER_ID']}/photo/$value", headers=headers)
    
    # Convert photo value to image
    img = Image.open(BytesIO(res.content))
    
    # Show image    
    img.show()

