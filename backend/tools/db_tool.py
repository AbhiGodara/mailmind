from crewai.tools import tool
from backend.db.database import SessionLocal
from backend.db.models import EmailSummary
import json

class DatabaseTools():
    @tool("Save Email Summary")
    def save_summary(data: str) -> str:
        """
        Saves an email summary to the PostgreSQL database.
        Input MUST be a JSON string with keys: thread_id, sender, subject, key_points, action_items, category, priority
        """
        try:
            parsed_data = json.loads(data)
            db = SessionLocal()
            
            summary = EmailSummary(
                thread_id=parsed_data.get('thread_id', ''),
                sender=parsed_data.get('sender', ''),
                subject=parsed_data.get('subject', ''),
                key_points=parsed_data.get('key_points', ''),
                action_items=parsed_data.get('action_items', ''),
                category=parsed_data.get('category', 'UNCATEGORIZED'),
                priority=parsed_data.get('priority', 'NORMAL')
            )
            db.add(summary)
            db.commit()
            db.refresh(summary)
            db.close()
            return f"Summary saved successfully with ID: {summary.id}"
        except json.JSONDecodeError:
            return "Error: Input must be a valid JSON string."
        except Exception as e:
            return f"Error saving summary to database: {str(e)}"
