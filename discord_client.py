# discord_client.py — Build Discord embeds and post/edit via webhook

import json
import urllib.request
import urllib.error
from datetime import datetime, timezone
from typing import Optional
from config import DISCORD_WEBHOOK, INDICATOR_COLOUR, INDICATOR_EMOJI

_HEADERS = {
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
}


def build_embed(summary):
    status      = summary.get("status", {})
    indicator   = status.get("indicator", "unknown")
    description = status.get("description", "Unknown")
    page_url    = summary.get("page", {}).get("url", "https://status.anthropic.com")

    colour = INDICATOR_COLOUR.get(indicator, INDICATOR_COLOUR["unknown"])
    emoji  = INDICATOR_EMOJI.get(indicator, "❓")
    now    = datetime.now(timezone.utc)

    # Active incidents (capped at 5)
    incident_lines = [
        f"• **[{i.get('name', 'Unnamed')}]({i.get('shortlink', page_url)})** "
        f"— {i.get('impact', 'unknown').capitalize()}"
        for i in summary.get("incidents", [])[:5]
    ]

    # Degraded components (capped at 8)
    component_lines = [
        f"• {c.get('name', 'Unknown')}: **{c.get('status', 'unknown').replace('_', ' ').title()}**"
        for c in summary.get("components", [])
        if c.get("status") not in ("operational", "") and not c.get("group", False)
    ][:8]

    fields = []
    if incident_lines:
        fields.append({"name": "🚧 Active Incidents",    "value": "\n".join(incident_lines),    "inline": False})
    if component_lines:
        fields.append({"name": "📉 Degraded Components", "value": "\n".join(component_lines), "inline": False})
    if not incident_lines and not component_lines and indicator == "none":
        fields.append({"name": "All Systems", "value": "All components are fully operational.", "inline": False})

    fields.append({
        "name":   "🕐 Last Checked",
        "value":  now.strftime("`%Y-%m-%d %H:%M UTC`"),
        "inline": False,
    })

    return {
        "title":     f"{emoji}  Anthropic Status — {description}",
        "url":       page_url,
        "color":     colour,
        "fields":    fields,
        "footer":    {"text": "Anthropic Status Monitor • status.anthropic.com"},
        "timestamp": now.isoformat(),
    }


def build_offline_embed(reason="The monitor script has stopped running."):
    now = datetime.now(timezone.utc)
    return {
        "title":       "⚫  Anthropic Status Monitor — OFFLINE",
        "description": f"_{reason}_",
        "color":       0x2C2F33,
        "fields": [
            {
                "name":   "⏹ Stopped At",
                "value":  now.strftime("`%Y-%m-%d %H:%M UTC`"),
                "inline": False,
            }
        ],
        "footer":    {"text": "Anthropic Status Monitor • status.anthropic.com"},
        "timestamp": now.isoformat(),
    }


def post_or_edit(embed, message_id=None):
    # type: (dict, Optional[str]) -> str
    payload = json.dumps({"embeds": [embed]}).encode("utf-8")

    if message_id:
        url    = f"{DISCORD_WEBHOOK}/messages/{message_id}"
        method = "PATCH"
    else:
        url    = f"{DISCORD_WEBHOOK}?wait=true"
        method = "POST"

    req = urllib.request.Request(url, data=payload, headers=_HEADERS, method=method)
    with urllib.request.urlopen(req, timeout=15) as resp:
        body = resp.read().decode()
        if resp.status not in (200, 204):
            raise RuntimeError(f"Discord returned HTTP {resp.status}: {body}")
        result = json.loads(body) if body else {}

    return result.get("id", message_id)
