# config.py — All constants and configuration

import os

# ── Load .env file ────────────────────────────────────────────────────────────
def _load_env() -> None:
    env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
    if not os.path.exists(env_path):
        return
    with open(env_path) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, _, val = line.partition("=")
                os.environ[key.strip()] = val.strip()

_load_env()

DISCORD_WEBHOOK = os.environ.get("DISCORD_WEBHOOK", "")
STATUS_API      = "https://status.anthropic.com/api/v2/summary.json"

# Discord embed sidebar colours (hex → int)
INDICATOR_COLOUR = {
    "none":        0x57F287,  # green  – all operational
    "minor":       0xFEE75C,  # yellow – minor outage
    "major":       0xED4245,  # red    – major outage
    "critical":    0x8B0000,  # dark red
    "maintenance": 0x5865F2,  # blue   – scheduled maintenance
    "unknown":     0x95A5A6,  # grey
}

INDICATOR_EMOJI = {
    "none":        "✅",
    "minor":       "⚠️",
    "major":       "🔴",
    "critical":    "🚨",
    "maintenance": "🔧",
    "unknown":     "❓",
}
