import os
from crewai.tools import tool
from twilio.rest import Client

class TwilioTools():
    @tool("Send WhatsApp Notification")
    def send_whatsapp(data: str) -> str:
        """
        Sends a WhatsApp notification to the user for high-priority emails.
        The input should be a pipe (|) separated string: sender|subject|summary.
        For example: "John Doe|Urgent Meeting|John wants to meet at 3 PM."
        """
        try:
            parts = data.split('|')
            if len(parts) != 3:
                return "Error: Input must be formatted as 'sender|subject|summary'"
            sender, subject, summary = parts
            
            account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
            auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
            from_whatsapp_number = os.environ.get('TWILIO_FROM_NUMBER')
            to_whatsapp_number = os.environ.get('TWILIO_TO_NUMBER')

            if not all([account_sid, auth_token, from_whatsapp_number, to_whatsapp_number]):
                return "Error: Twilio credentials are not fully configured in the environment."

            client = Client(account_sid, auth_token)
            message_body = f"🚀 *HIGH PRIORITY EMAIL*\n\n*From:* {sender}\n*Subject:* {subject}\n\n*Summary:* {summary}"
            
            message = client.messages.create(
                body=message_body,
                from_=f"whatsapp:{from_whatsapp_number}",
                to=f"whatsapp:{to_whatsapp_number}"
            )
            return f"WhatsApp notification sent successfully. Message SID: {message.sid}"
        except Exception as e:
            return f"Error sending WhatsApp message: {str(e)}"
