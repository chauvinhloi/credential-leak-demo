import json
import os
from datetime import datetime, timezone
from pathlib import Path


def _mask(value: str) -> str:
    if not value:
        return "missing"
    if len(value) <= 4:
        return "*" * len(value)
    return f"{value[:2]}{'*' * (len(value) - 4)}{value[-2:]}"


def simulate_exfiltration():
    client_id = os.getenv("DEMO_DATABRICKS_CLIENT_ID", "")
    client_secret = os.getenv("DEMO_DATABRICKS_CLIENT_SECRET", "")
    sink_path = Path(os.getenv("DEMO_EXFIL_SINK", "/tmp/databricks-demo-exfil.log"))
    sink_path.parent.mkdir(parents=True, exist_ok=True)

    payload = {
        "event": "simulated_dependency_exfiltration",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "note": "This is a safe demo. Only demo-prefixed variables are read.",
        "demo_client_id": client_id,
        "demo_client_secret": client_secret,
    }

    print(json.dumps(payload, indent=4))
