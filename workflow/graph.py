from dotenv import load_dotenv
load_dotenv()

from langgraph.graph import StateGraph, END

from workflow.state import EmailsState
from workflow.nodes import Nodes
from crew.crew import EmailFilterCrew

class WorkFlow():
    def __init__(self):
        nodes = Nodes()
        workflow = StateGraph(EmailsState)

        workflow.add_node("check_new_emails", nodes.check_email)
        workflow.add_node("draft_responses", EmailFilterCrew().kickoff)

        workflow.set_entry_point("check_new_emails")
        workflow.add_conditional_edges(
                "check_new_emails",
                nodes.new_emails,
                {
                    "continue": 'draft_responses',
                    "end": END
                }
        )
        workflow.add_edge('draft_responses', END)
        self.app = workflow.compile()
