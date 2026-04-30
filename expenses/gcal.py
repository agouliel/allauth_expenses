# https://gemini.google.com/app/9b94784266792b1e
from allauth.socialaccount.models import SocialToken, SocialApp
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

def get_calendar_service(user):
    # 1. Get the token from the database
    token_obj = SocialToken.objects.filter(
        account__user=user, 
        account__provider='google'
    ).first()

    if not token_obj:
        return None

    # 2. Get the App credentials (ID and Secret) to allow refreshing
    app = SocialApp.objects.get(provider='google')

    # 3. Build the Credentials object
    creds = Credentials(
        token=token_obj.token,
        refresh_token=token_obj.token_secret,
        token_uri='https://oauth2.googleapis.com/token',
        client_id=app.client_id,
        client_secret=app.secret,
        scopes=['https://www.googleapis.com/auth/calendar.readonly']
    )

    # 4. Refresh the token if it's expired
    if creds.expired and creds.refresh_token:
        creds.refresh(Request())
        # Update the database with the new access token and expiration
        token_obj.token = creds.token
        token_obj.expires_at = creds.expiry
        token_obj.save()

    # 5. Build the Calendar Service
    return build('calendar', 'v3', credentials=creds)