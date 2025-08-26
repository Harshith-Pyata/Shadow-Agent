# for authentication even below one works but due to http or https it is blocking the authentication so use below code
from langchain_google_community import GmailToolkit
from langchain_google_community.gmail.utils import build_resource_service

toolkit = GmailToolkit()

from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
import os

SCOPES = ["https://mail.google.com/"]
TOKEN_PATH = "token.json"
CLIENT_SECRET = "credentials.json"

if os.path.exists(TOKEN_PATH):
    credentials = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
else:
    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET, SCOPES)
    credentials = flow.run_console()  # <== Fixes the local server issue
    with open(TOKEN_PATH, "w") as token:
        token.write(credentials.to_json())

api_resource = build_resource_service(credentials=credentials)
toolkit = GmailToolkit(api_resource=api_resource)


from langchain_google_community import GmailToolkit

toolkit = GmailToolkit()

# need only while authenticating

from langchain_google_community.gmail.utils import (
    build_resource_service,
    get_gmail_credentials,
)

# Can review scopes here https://developers.google.com/gmail/api/auth/scopes
# For instance, readonly scope is 'https://www.googleapis.com/auth/gmail.readonly'
credentials = get_gmail_credentials(
    token_file="token.json",
    scopes=["https://mail.google.com/"],
    client_secrets_file="credentials.json",
)
api_resource = build_resource_service(credentials=credentials)
emailkit = GmailToolkit(api_resource=api_resource).get_tools()