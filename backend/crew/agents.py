from langchain_community.agent_toolkits import GmailToolkit
from langchain_community.tools.gmail.get_thread import GmailGetThread
from langchain_community.tools.tavily_search import TavilySearchResults

from textwrap import dedent
from crewai import Agent
from backend.crew.tools import CreateDraftTool
from backend.tools.twilio_tool import TwilioTools
from backend.tools.calendar_tool import CalendarTools
from backend.tools.db_tool import DatabaseTools
from backend.tools.approval_tool import ApprovalTools

class EmailFilterAgents():
    def __init__(self):
        self.gmail = GmailToolkit()

    def email_filter_agent(self):
        return Agent(
            role='Senior Email Analyst',
            goal='Filter out non-essential emails like newsletters and promotional content',
            backstory=dedent("""\
                As a Senior Email Analyst, you have extensive experience in email content analysis.
                You are adept at distinguishing important emails from spam, newsletters, and other
                irrelevant content. Your expertise lies in identifying key patterns and markers that
                signify the importance of an email."""),
            verbose=True,
            allow_delegation=False
        )

    def email_action_agent(self):
        return Agent(
            role='Email Action Specialist',
            goal='Identify action-required emails, classify their priority (HIGH, NORMAL), and compile a list of their IDs',
            backstory=dedent("""\
                With a keen eye for detail and a knack for understanding context, you specialize
                in identifying emails that require immediate action. Your skill set includes interpreting
                the urgency and importance of an email based on its content and context. You always
                flag highly urgent emails as 'HIGH' priority."""),
            tools=[
                GmailGetThread(api_resource=self.gmail.api_resource),
                TavilySearchResults()
            ],
            verbose=True,
            allow_delegation=False,
        )

    def email_response_writer(self):
        return Agent(
            role='Email Response Writer',
            goal='Draft responses to action-required emails',
            backstory=dedent("""\
                You are a skilled writer, adept at crafting clear, concise, and effective email responses.
                Your strength lies in your ability to communicate effectively, ensuring that each response is
                tailored to address the specific needs and context of the email. You ALWAYS request human
                approval before saving or sending a draft using the Request Human Approval tool."""),
            tools=[
                TavilySearchResults(),
                GmailGetThread(api_resource=self.gmail.api_resource),
                ApprovalTools.request_approval,
                CreateDraftTool.create_draft
            ],
            verbose=True,
            allow_delegation=False,
        )

    def notifier_agent(self):
        return Agent(
            role='Urgent Notification Specialist',
            goal='Send WhatsApp notifications for HIGH priority emails',
            backstory=dedent("""\
                You are responsible for making sure the user is immediately notified about highly
                urgent emails via WhatsApp. You extract the key details and send a succinct summary."""),
            tools=[TwilioTools.send_whatsapp],
            verbose=True,
            allow_delegation=False,
        )

    def calendar_agent(self):
        return Agent(
            role='Calendar Management Specialist',
            goal='Extract meeting details from emails and schedule Google Calendar events',
            backstory=dedent("""\
                You are an executive assistant who excels at identifying dates, times, locations,
                and meeting topics from emails. You create calendar events accurately. You ALWAYS
                request human approval before creating a calendar event using the Request Human Approval tool."""),
            tools=[
                ApprovalTools.request_approval,
                CalendarTools.create_event
            ],
            verbose=True,
            allow_delegation=False,
        )

    def summarization_agent(self):
        return Agent(
            role='Email Summarization Specialist',
            goal='Create structured summaries for every email and save them to the database',
            backstory=dedent("""\
                You read through emails and summarize their key points and action items.
                You are meticulous about storing this structured data into the database for analytics."""),
            tools=[
                DatabaseTools.save_summary
            ],
            verbose=True,
            allow_delegation=False,
        )
