This is demo code to download transcripts of meeting calls via Graph API (see the tutorial [Get meeting transcripts using Graph APIs](https://docs.microsoft.com/en-us/microsoftteams/platform/graph-api/meeting-transcripts/overview-transcripts) for details).
Please be aware of following prerequesites:

# Service Principal
- Create Service Principal in AAD tenant.
- Assign secret to Service Principal.
- Assign Graph API permissions to Service Principal:
    - CallRecords.Read.All
    - OnlineMeetings.Read.All
    - OnlineMeetingTranscript.Read.All

# Define Application Access Policy for your Service Principal

## Install required Powershell extension
see [Manage Skype for Business Online with PowerShell](https://docs.microsoft.com/en-us/microsoft-365/enterprise/manage-skype-for-business-online-with-microsoft-365-powershell?view=o365-worldwide)
```
Install-Module MicrosoftTeams -Scope CurrentUser
Connect-MicrosoftTeams
```
 
## Create Application Access Policy
see [Configure application access to online meetings](https://docs.microsoft.com/en-us/graph/cloud-communication-online-meeting-application-access-policy)
```
$PolicyName="AAB_graph_teams-transcripts_to_-Online-Meetings_Global"
New-CsApplicationAccessPolicy -Identity $PolicyName -AppIds "[APP ID OF YOUR SERVICE PRINCIPAL HERE]" -Description "This policy allows SP graph_teams-transcripts to access all online meetings."
Grant-CsApplicationAccessPolicy -PolicyName $PolicyName -Global
```

# Define environment variables
- Get ID of meeting ID.
  - Either from event sent, for example, to Azure Function.
  - Or -- for testing purposes -- from Microsoft Teams Admin Center (_Note_ It might take some minutes after a meeting has ended until it appears in the admin center):
    - Go to "Manage Users".
    - Navigate to meeting organizer.
    - Navigate to 'Meetings & calls'
    - In table 'Past Meetings' wait for meeting and get meeting ID from the first column.

# Test it
- Create a new virtual environment
  ```
  python3 -m venv env
  ```
- Install required packages
  ```
  pip install -r requirements.txt
  ```
- Either run code with VS Code or from console.
  - From VS Code:
    - Open in VS Code
    - Install Python Extension.
    - Create file with name `.env` in project directory with following content:
      ```
      TENANT_ID=[TENANT ID HERE]
      CLIENT_ID=[SERVICE PRINCIPAL'S APP ID]
      CLIENT_SECRET=[SERVICE PRINCIPAL'S SECRET HERE]
      MEETING_ID=[MEETING ID FROM TEAMS ADMIN PORTAL HERE]
      ```
    - Create launch configuration and launch code.
  - From console: 
    - Export environment variables:
      ```
      export TENANT_ID=[TENANT ID HERE]
      export CLIENT_ID=[SERVICE PRINCIPAL'S APP ID]
      export CLIENT_SECRET=[SERVICE PRINCIPAL'S SECRET HERE]
      export MEETING_ID=[MEETING ID FROM TEAMS ADMIN PORTAL HERE]
      ```
    - Run python application:
      ```
      python3 ./pull-transcripts.py
      ```
