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
                """),
            expected_output="A bulleted list of relevant thread_ids and the sender.",
            agent=agent
        )

    def action_required_emails_task(self, agent):
        return Task(
            description=dedent("""\
                For each email thread, pull and analyze the complete threads using only the actual Thread ID.
                understand the context, key points, and the overall sentiment of the conversation.

                Identify the main query or concerns that needs to be addressed in the response for each.
                IMPORTANT: You must classify the priority of the email as either 'HIGH' or 'NORMAL'.
                """),
            expected_output="A list for all emails with thread_id, summary, main points, user, style, sender, and priority.",
            agent=agent
        )

    def draft_responses_task(self, agent):
        return Task(
            description=dedent(f"""\
                Based on the action-required emails identified, draft responses for each.
                Ensure that each response is tailored to address the specific needs and context.

                - Assume the persona of the user and mimic the communication style.
                - Do research IF NECESSARY BEFORE drafting.
                - Use the Create Draft tool directly to save the draft.
                """),
            expected_output="A confirmation that all responses have been handled.",
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
                """),
            expected_output="A confirmation that all emails have been summarized.",
            agent=agent
        )

    def notify_high_priority_task(self, agent):
        return Task(
            description=dedent("""\
                Review the list of analyzed emails. For ANY email that has a priority of 'HIGH',
                use the Send WhatsApp Notification tool to alert the user.
                Pass the input formatted as "sender|subject|summary".
                """),
            expected_output="A confirmation of which notifications were sent.",
            agent=agent
        )

    def extract_calendar_events_task(self, agent):
        return Task(
            description=dedent("""\
                Review the analyzed emails for any mention of dates, times, locations, and meeting titles.
                If a meeting or event is detected with sufficient confidence:
                ONLY create events for confirmed meeting invitations with clear start and end times. DO NOT create events for job application follow-ups, general dates, or deadlines.
                Use the Create Calendar Event tool directly to add it to the calendar. Provide a JSON string with 
                summary, start_time, end_time, location, and description.
                """),
            expected_output="A confirmation of any calendar events created.",
            agent=agent
        )

    def export_data_task(self, agent):
        return Task(
            description=dedent("""\
                Review all the processed and analyzed emails, drafts, and calendar events from this session.
                For EACH email that was processed, you MUST use the Append to JSON file tool.
                Provide a JSON string containing the following keys:
                - email_id
                - sender
                - date (if available, else 'Unknown')
                - type (category like PROMOTION, WORK, etc.)
                - priority (HIGH or NORMAL)
                - draft (the drafted response, or 'None' if skipped)
                - summary (the brief summary of the email)
                - whatsapp_msg (Set to 'Yes' IF AND ONLY IF priority is exactly 'HIGH'. If priority is 'NORMAL', this MUST be 'No')
                - calendar_event (Details of the event added, or 'None' if no confirmed meeting)
                - action_items (Key things to do based on the email)
                - sentiment (Positive, Negative, Neutral)
                - category (More specific category classification)
                - is_promotional (True or False)
                """),
            expected_output="A confirmation that all processed emails have been exported to the JSON file.",
            agent=agent
        )
