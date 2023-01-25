from datetime import timedelta, date, datetime
import os.path
import json

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from .release import Release


class Calendar:
    SCOPES = ['https://www.googleapis.com/auth/calendar']
    creds = None

    def __init__(self):
        if os.path.exists('token.json'):
            self.creds = Credentials.from_authorized_user_file('token.json', self.SCOPES)
        if not self.creds or not self.creds.valid:
            self.authenticate()
        self.service = build('calendar', 'v3', credentials=self.creds)
        self._id = None
        self._events = None

    def authenticate(self):
        if self.creds and self.creds.expired and self.creds.refresh_token:
            self.creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', self.SCOPES)
            self.creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(self.creds.to_json())

    @property
    def id(self) -> str:
        if self._id is not None:
            return self._id
        if os.path.exists('calendar.json'):
            with open('calendar.json', 'r') as f:
                self._id = json.load(f)['id']
                return self._id
        body = {
            "summary": "Crunchyroll Releases",
            "timezone": "Europe/Paris",
        }
        resource = self.service.calendars().insert(body=body).execute()
        self._id = resource['id']
        with open('calendar.json', 'w') as f:
            json.dump(resource, f, indent=2)
        return self._id

    @property
    def start_of_week(self) -> datetime:
        today = date.today()
        start_date = today - timedelta(today.isoweekday() - 1)
        return datetime(
            start_date.year, start_date.month, start_date.day,
            0, 0, 0, 0,
        )

    @property
    def end_of_week(self) -> datetime:
        start = self.start_of_week
        end = start + timedelta(days=7)
        return datetime(
            end.year, end.month, end.day,
            23, 59, 59, 0,
        )

    @property
    def events(self) -> dict:
        if self._events is None:
            self._events = self.service.events().list(
                calendarId=self.id,
                # timeMin=self.start_of_week.isoformat(),
                # timeMax=self.end_of_week.isoformat(),
                maxResults=2500,
            ).execute()
        return self._events

    def is_release_added(self, release: Release) -> bool:
        for event in self.events['items']:
            if event['summary'] == release.event_name:
                return True
        return False

    def add_release(self, release: Release) -> None:
        if self.is_release_added(release):
            return

        event = {
            'summary': release.event_name,
            'description': release.url,
            'start': {
                'dateTime': release.datetime_start.isoformat(),
                'timeZone': 'Europe/Paris',
            },
            'end': {
                'dateTime': release.datetime_end.isoformat(),
                'timeZone': 'Europe/Paris',
            },
            'reminders': {
                'useDefault': False,
                'overrides': [
                    {'method': 'popup', 'minutes': 10},
                ],
            },
        }
        self.service.events().insert(calendarId=self.id, body=event).execute()
