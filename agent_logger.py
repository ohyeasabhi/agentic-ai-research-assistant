import json
from datetime import datetime
from pathlib import Path

LOG_FILE = Path("agent_logs.json")


def log_run(
    topic: str,
    model: str,
    retries: int,
    tools_used: list,
    duration_sec: float
):
    entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "topic": topic,
        "model": model,
        "retries": retries,
        "tools_used": tools_used,
        "duration_sec": round(duration_sec, 2)
    }

    if LOG_FILE.exists():
        logs = json.loads(LOG_FILE.read_text())
    else:
        logs = []

    logs.append(entry)
    LOG_FILE.write_text(json.dumps(logs, indent=2))
