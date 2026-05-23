import os
from langchain_community.agent_toolkits import GmailToolkit
from langchain_community.tools.gmail.search import GmailSearch
from langchain_community.tools.gmail.utils import get_gmail_credentials, build_resource_service

class Nodes():
    def __init__(self):
        # We must load the credentials with the exact same scopes used to generate token.json
        # otherwise Google OAuth throws an 'invalid_scope' error during token refresh.
        scopes = [
            'https://www.googleapis.com/auth/gmail.modify',
            'https://www.googleapis.com/auth/calendar'
        ]
        credentials = get_gmail_credentials(
            token_file="token.json",
            scopes=scopes,
            client_secrets_file="credentials.json"
        )
        api_resource = build_resource_service(credentials=credentials)
        self.gmail = GmailToolkit(api_resource=api_resource)

    def check_email(self, state):
        print("# Checking for new emails")
        search = GmailSearch(api_resource=self.gmail.api_resource)
        emails = search._run(query='newer_than:1d')
        redis_url = os.environ.get("REDIS_URL", "redis://redis:6379/0")
        try:
            import redis
            r = redis.Redis.from_url(redis_url, decode_responses=True)
            r.ping() # test connection
            redis_available = True
        except Exception as e:
            print(f"Redis not available for caching emails: {e}")
            redis_available = False

        checked_emails = state.get('checked_emails_ids', [])
        thread = []
        new_emails = []
        for email in emails:
            # Check Redis to see if we processed this exact email in a previous run
            is_processed = False
            if redis_available and r.get(f"processed_email:{email['id']}"):
                is_processed = True

            sender = email.get('sender', '')
            my_email = os.environ.get('MY_EMAIL', '')

            if email['id'] in checked_emails:
                pass # Already checked in this session
            elif is_processed:
                pass # Already processed in a past session
            elif email['threadId'] in thread:
                pass # Already got an email from this thread
            elif my_email and my_email in sender:
                print(f"  -> Skipping email from yourself: {sender}")
            else:
                print(f"  -> Found NEW email from: {sender}")
                thread.append(email['threadId'])
                new_emails.append(
                    {
                        "id": email['id'],
                        "threadId": email['threadId'],
                        "snippet": email['snippet'],
                        "sender": sender
                    }
                )
                if redis_available:
                    # Remember this email was processed for 48 hours
                    r.set(f"processed_email:{email['id']}", "1", ex=172800)

        checked_emails.extend([email['id'] for email in emails])
        return {
            **state,
            "emails": new_emails,
            "checked_emails_ids": checked_emails
        }

    def new_emails(self, state):
        if len(state['emails']) == 0:
            print("## No new emails")
            return "end"
        else:
            print("## New emails")
            return "continue"
