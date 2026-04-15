# status_client.py — Fetch Anthropic status and build a change-detection snapshot

import json
import urllib.request
from config import STATUS_API


def fetch() -> dict:
    """Fetch the full summary JSON from the Anthropic status page."""
    req = urllib.request.Request(
        STATUS_API,
        headers={"User-Agent": "claude-status-monitor/1.0"},
    )
    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.loads(resp.read().decode())


def snapshot(summary: dict) -> dict:
    """Minimal fingerprint used to detect changes between runs."""
    indicator = summary.get("status", {}).get("indicator", "unknown")
    incident_ids = sorted(i.get("id") for i in summary.get("incidents", []))
    degraded_ids = sorted(
        c.get("id")
        for c in summary.get("components", [])
        if c.get("status") not in ("operational", "") and not c.get("group", False)
    )
    return {
        "indicator": indicator,
        "incident_ids": incident_ids,
        "degraded_ids": degraded_ids,
    }
