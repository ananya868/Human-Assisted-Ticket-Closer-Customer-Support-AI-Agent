import logging

class CRMTool:
    @staticmethod
    def update_ticket_status(ticket_id: str, status: str):
        logging.info(f"CRM: Updating ticket {ticket_id} to status: {status}")
        return True

class EmailTool:
    @staticmethod
    def send_response(customer_email: str, content: str):
        logging.info(f"Email: Sending response to {customer_email}")
        print(f"\n--- SENT EMAIL TO {customer_email} ---\n{content}\n---------------------------\n")
        return True
