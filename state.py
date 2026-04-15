# state.py — Persist and load the last-known status snapshot + Discord message ID

import json
import os
from typing import Optional

STATE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "status_state.json")


def load():
    # type: () -> dict
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError):
            pass
    return {}


def save(snapshot, message_id=None):
    # type: (dict, Optional[str]) -> None
    data = dict(snapshot)
    if message_id:
        data["message_id"] = message_id
    with open(STATE_FILE, "w") as f:
        json.dump(data, f, indent=2)


def get_message_id():
    # type: () -> Optional[str]
    return load().get("message_id")
