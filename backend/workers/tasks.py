from backend.workers.celery_app import app
from backend.workflow.graph import WorkFlow
from backend.workflow.state import EmailsState

@app.task
def poll_gmail():
    print("Polling Gmail for new emails...")
    workflow_app = WorkFlow().app
    # Initialize the state. The check_new_emails node will search for new emails.
    initial_state = EmailsState(
        checked_emails_ids=[], 
        emails=[], 
        action_required_emails={}
    )
    result = workflow_app.invoke(initial_state)
    print("Workflow execution completed.")
    return "Success"
