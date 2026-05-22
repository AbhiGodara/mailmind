import os
import json
from langchain.tools import tool
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

class CalendarTools():
    @tool("Create Calendar Event")
    def create_event(data: str) -> str:
        """
        Creates a Google Calendar event.
        Input MUST be a JSON string with keys: summary, start_time, end_time, location, description.
        Time format MUST be ISO formatted string like '2026-05-28T09:00:00-07:00'.
        """
        try:
            parsed_data = json.loads(data)
            creds = None
            if os.path.exists('token.json'):
                # Note: token must have 'https://www.googleapis.com/auth/calendar' scope
                creds = Credentials.from_authorized_user_file('token.json')
            else:
                return "Error: token.json not found. OAuth must be completed first."

            service = build('calendar', 'v3', credentials=creds)

            event = {
                'summary': parsed_data.get('summary'),
                'location': parsed_data.get('location', ''),
                'description': parsed_data.get('description', ''),
                'start': {
                    'dateTime': parsed_data.get('start_time'),
                    'timeZone': 'UTC',
                },
                'end': {
                    'dateTime': parsed_data.get('end_time'),
                    'timeZone': 'UTC',
                },
            }

            event = service.events().insert(calendarId='primary', body=event).execute()
            return f"Event created: {event.get('htmlLink')}"
        except Exception as e:
            return f"Error creating calendar event: {str(e)}"
