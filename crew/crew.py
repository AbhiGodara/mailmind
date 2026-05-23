from crewai import Crew

from crew.agents import EmailFilterAgents
from crew.tasks import EmailFilterTasks

class EmailFilterCrew():
    def __init__(self):
        agents = EmailFilterAgents()
        self.filter_agent = agents.email_filter_agent()
        self.action_agent = agents.email_action_agent()
        self.writer_agent = agents.email_response_writer()
        self.notifier_agent = agents.notifier_agent()
        self.calendar_agent = agents.calendar_agent()
        self.summarization_agent = agents.summarization_agent()
        self.export_agent = agents.export_data_agent()

    def kickoff(self, state):
        print("### Filtering emails")
        tasks = EmailFilterTasks()
        
        formatted_emails = self._format_emails(state['emails'])

        crew = Crew(
            agents=[
                self.filter_agent, 
                self.summarization_agent,
                self.action_agent, 
                self.notifier_agent,
                self.calendar_agent,
                self.writer_agent,
                self.export_agent
            ],
            tasks=[
                tasks.filter_emails_task(self.filter_agent, formatted_emails),
                tasks.summarize_emails_task(self.summarization_agent, formatted_emails),
                tasks.action_required_emails_task(self.action_agent),
                tasks.notify_high_priority_task(self.notifier_agent),
                tasks.extract_calendar_events_task(self.calendar_agent),
                tasks.draft_responses_task(self.writer_agent),
                tasks.export_data_task(self.export_agent)
            ],
            verbose=True
        )
        result = crew.kickoff()
        return {**state, "action_required_emails": result}

    def _format_emails(self, emails):
        emails_string = []
        for email in emails:
            print(email)
            arr = [
                f"ID: {email['id']}",
                f"- Thread ID: {email['threadId']}",
                f"- Snippet: {email['snippet']}",
                f"- From: {email['sender']}",
                f"--------"
            ]
            emails_string.append("\n".join(arr))
        return "\n".join(emails_string)
