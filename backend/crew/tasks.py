from crewai import Task
from textwrap import dedent

class EmailFilterTasks:
    def filter_emails_task(self, agent, emails):
        return Task(
            description=dedent(f"""\
                Analyze a batch of emails and filter out non-essential ones such as newsletters, 
                promotional content and notifications.

                Use your expertise in email content analysis to distinguish
                important emails from the rest, pay attention to the sender and avoid invalid emails.

                Make sure to filter for the messages actually directed at the user and avoid notifications.

                EMAILS
                -------
                {emails}

                Your final answer MUST be a list of relevant thread_ids and the sender, use bullet points.
                """),
            agent=agent
        )

    def action_required_emails_task(self, agent):
        return Task(
            description=dedent("""\
                For each email thread, pull and analyze the complete threads using only the actual Thread ID.
                understand the context, key points, and the overall sentiment of the conversation.

                Identify the main query or concerns that needs to be addressed in the response for each.
                IMPORTANT: You must classify the priority of the email as either 'HIGH' or 'NORMAL'.

                Your final answer MUST be a list for all emails with:
                - the thread_id
                - a summary of the email thread
                - a highlighting with the main points
                - identify the user and who he will be answering to
                - communication style in the thread
                - the sender's email address
                - priority (HIGH or NORMAL)
                """),
            agent=agent
        )

    def draft_responses_task(self, agent):
        return Task(
            description=dedent(f"""\
                Based on the action-required emails identified, draft responses for each.
                Ensure that each response is tailored to address the specific needs and context.

                - Assume the persona of the user and mimic the communication style.
                - Do research IF NECESSARY BEFORE drafting.
                - You MUST use the Request Human Approval tool before creating a draft. Pass a description like "Draft response to [Sender]: [Subject]".
                - ONLY if approved, use the tool provided to create the draft.

                Your final answer MUST be a confirmation that all responses have been handled.
                """),
            agent=agent
        )

    def summarize_emails_task(self, agent, emails):
        return Task(
            description=dedent(f"""\
                Process ALL of these incoming emails and extract structured summaries.
                
                EMAILS
                -------
                {emails}

                For EACH email, use the Save Email Summary tool. Provide the tool with a JSON string 
                containing: thread_id, sender, subject, key_points (max 3 bullets), action_items, category, priority.
                
                Your final answer MUST be a confirmation that all emails have been summarized.
                """),
            agent=agent
        )

    def notify_high_priority_task(self, agent):
        return Task(
            description=dedent("""\
                Review the list of analyzed emails. For ANY email that has a priority of 'HIGH',
                use the Send WhatsApp Notification tool to alert the user.
                Pass the input formatted as "sender|subject|summary".

                Your final answer MUST confirm which notifications were sent.
                """),
            agent=agent
        )

    def extract_calendar_events_task(self, agent):
        return Task(
            description=dedent("""\
                Review the analyzed emails for any mention of dates, times, locations, and meeting titles.
                If a meeting or event is detected with sufficient confidence:
                1. Use the Request Human Approval tool passing "Create calendar event: [Title] at [Time]".
                2. If approved, use the Create Calendar Event tool. Provide a JSON string with 
                   summary, start_time, end_time, location, and description.

                Your final answer MUST confirm any calendar events created.
                """),
            agent=agent
        )
