# src/gmail/auth.py
import os
import pickle
from pathlib import Path

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ['https://www.googleapis.com/auth/gmail.modify']
OOB_REDIRECT_URI = 'urn:ietf:wg:oauth:2.0:oob'

BASE_DIR = Path(__file__).resolve().parents[2]
TOKEN_PATH = BASE_DIR / 'token.pickle'
CREDENTIALS_PATH = BASE_DIR / 'credentials.json'


def get_creds():
    """Authenticate and return valid Gmail API credentials using manual OOB flow."""
    creds = None

    if TOKEN_PATH.exists():
        with TOKEN_PATH.open('rb') as token:
            creds = pickle.load(token)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not CREDENTIALS_PATH.exists():
                raise FileNotFoundError(
                    f"Google OAuth credentials file not found at {CREDENTIALS_PATH}. "
                    "Please place credentials.json in the project root."
                )

            # Create the flow with explicit OOB redirect URI
            flow = InstalledAppFlow.from_client_secrets_file(
                str(CREDENTIALS_PATH),
                SCOPES,
                redirect_uri=OOB_REDIRECT_URI
            )
            
            # Generate auth URL (will include redirect_uri)
            auth_url, _ = flow.authorization_url(prompt='consent')
            print('Please go to this URL and authorize access:')
            print(auth_url)
            
            # Get the authorization code
            code = input('Enter the authorization code: ')
            
            # Exchange code for credentials
            flow.fetch_token(code=code)
            creds = flow.credentials
        
        # Save credentials for next run
        with TOKEN_PATH.open('wb') as token:
            pickle.dump(creds, token)
    
    return creds