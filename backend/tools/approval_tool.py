import os
import time
import uuid
import redis
from langchain.tools import tool

class ApprovalTools():
    @tool("Request Human Approval")
    def request_approval(action_description: str) -> str:
        """
        Pauses the agent and requests human approval before proceeding with a destructive or outbound action.
        Pass a detailed description of the action to be approved.
        Returns 'approved' if the human approves, or 'rejected' if the human rejects.
        """
        action_id = str(uuid.uuid4())
        redis_url = os.environ.get("REDIS_URL", "redis://localhost:6379/0")
        
        try:
            redis_client = redis.Redis.from_url(redis_url, decode_responses=True)
        except Exception as e:
            print(f"Warning: Redis not available ({e}). Assuming approved for local dev.")
            return "approved"

        # Mark action as pending
        redis_client.set(f"approval:{action_id}", "pending", ex=86400)
        
        print(f"\n==============================================")
        print(f"🛑 HUMAN APPROVAL REQUIRED 🛑")
        print(f"Action: {action_description}")
        print(f"Action ID: {action_id}")
        print(f"Approve via API: POST /api/approve with {{'action_id': '{action_id}', 'decision': 'approve'}}")
        print(f"==============================================\n")
        
        # Check if we are in local CLI dev mode
        if os.environ.get("DEV_MODE") == "True":
            decision = input(f"Approve this action? (y/n): ")
            if decision.lower() in ['y', 'yes']:
                return "approved"
            return "rejected"

        # Poll Redis for a decision
        max_wait = 300 # 5 minutes
        waited = 0
        while waited < max_wait:
            status = redis_client.get(f"approval:{action_id}")
            if status == "approve":
                return "approved"
            elif status == "reject":
                return "rejected"
            time.sleep(5)
            waited += 5
            
        return "rejected (timeout)"
