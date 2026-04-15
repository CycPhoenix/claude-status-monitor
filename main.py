#!/usr/bin/env python3
"""
main.py — Continuous 24/7 Anthropic status monitor.

Run:  python3 main.py
- Checks every 5 minutes
- Edits the same Discord message on every check (updates "Last Checked" time)
- Posts an OFFLINE embed if the script crashes or is stopped
Press Ctrl+C to stop.
"""

import sys
import os
import time
import signal
from datetime import datetime, timezone

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import state
import status_client
import discord_client
from config import DISCORD_WEBHOOK

CHECK_INTERVAL = 300  # 5 minutes


def post_offline(reason="Monitor stopped by user."):
    message_id = state.get_message_id()
    if not message_id:
        return
    try:
        embed = discord_client.build_offline_embed(reason)
        discord_client.post_or_edit(embed, message_id)
        print(f"  ⚫ Offline embed posted.")
    except Exception as exc:
        print(f"  WARNING: Could not post offline embed — {exc}")


def check() -> None:
    print(f"[{datetime.now(timezone.utc).isoformat()}] Checking Anthropic status…")

    try:
        summary = status_client.fetch()
    except Exception as exc:
        print(f"  WARNING: Could not fetch status API — {exc}")
        return

    current    = status_client.snapshot(summary)
    saved      = state.load()
    previous   = {k: v for k, v in saved.items() if k != "message_id"}
    message_id = saved.get("message_id")

    # Always update the embed to refresh "Last Checked" timestamp
    embed = discord_client.build_embed(summary)
    try:
        message_id = discord_client.post_or_edit(embed, message_id)
        action = "Edited" if saved.get("message_id") else "Posted new"
        changed = current != previous
        print(f"  ✅ {action} message (id={message_id}){' — status changed' if changed else ''}.")
    except Exception as exc:
        print(f"  ERROR: Discord post/edit failed — {exc}")
        return

    state.save(current, message_id)


def main() -> None:
    if not DISCORD_WEBHOOK or DISCORD_WEBHOOK == "your_webhook_url_here":
        print("ERROR: DISCORD_WEBHOOK is not set. Add it to the .env file.", file=sys.stderr)
        sys.exit(1)

    # Post offline embed on Ctrl+C or SIGTERM
    def handle_exit(sig, frame):
        print("\nShutting down…")
        post_offline("Monitor stopped by user (Ctrl+C / shutdown).")
        sys.exit(0)

    signal.signal(signal.SIGINT,  handle_exit)
    signal.signal(signal.SIGTERM, handle_exit)

    print("=" * 50)
    print("  Anthropic Status Monitor — running 24/7")
    print(f"  Checking every {CHECK_INTERVAL // 60} minutes")
    print("  Press Ctrl+C to stop")
    print("=" * 50)

    while True:
        try:
            check()
        except Exception as exc:
            print(f"  Unexpected error: {exc}")
            post_offline(f"Monitor encountered an unexpected error: {exc}")
            sys.exit(1)

        time.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    main()
