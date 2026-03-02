from dotenv import load_dotenv
load_dotenv()

from agents.flow import app
from models.schema import Ticket
import uuid


def run_demo():
    print("=== Human-Assisted AI Support Ticket Closer Demo ===\n")
    
    # 1. Simulate an incoming ticket
    test_ticket = Ticket(
        id=str(uuid.uuid4()),
        subject="Login Issue",
        description="I cannot log into my account. It says password incorrect but I'm sure it's right.",
        customer_id="CUST-123"
    )
    
    # 2. Run the workflow
    inputs = {"ticket": test_ticket, "history": []}
    for output in app.stream(inputs):
        # Stream the nodes for better visibility
        for key, value in output.items():
            print(f"Node '{key}' completed.")

if __name__ == "__main__":
    run_demo()
