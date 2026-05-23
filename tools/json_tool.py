import json
import os
from crewai.tools import tool

class JSONExportTools():
    @tool("Append to JSON file")
    def append_to_json(data: str) -> str:
        """
        Appends processed email data to processed_emails.json in the project root.
        Input MUST be a JSON string with the following keys:
        email_id, sender, date, type, priority, draft, summary, whatsapp_msg, calendar_event, action_items, sentiment, category, is_promotional
        """
        file_path = "processed_emails.json"
        
        try:
            parsed_data = json.loads(data)
        except json.JSONDecodeError:
            return "Error: Input must be a valid JSON string."
            
        existing_data = []
        if os.path.exists(file_path):
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read().strip()
                    if content:
                        existing_data = json.loads(content)
            except Exception as e:
                return f"Error reading existing JSON file: {e}"
                
        existing_data.append(parsed_data)
        
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(existing_data, f, indent=4, ensure_ascii=False)
            return f"Successfully appended data to {file_path}"
        except Exception as e:
            return f"Error writing to JSON file: {e}"
