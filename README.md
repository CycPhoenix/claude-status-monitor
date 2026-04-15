# 🔍 claude-status-monitor

> Real-time Anthropic / Claude status alerts delivered straight to your Discord server.

Watches the [Anthropic status page](https://status.anthropic.com) every 5 minutes and keeps a single Discord message up to date — no spam, just one clean embed that edits itself in place.

---

## ✨ Features

| | |
|---|---|
| 🔄 **Live updates** | Checks Anthropic's API every 5 minutes |
| 📌 **Single message** | Edits one Discord embed in place — no channel clutter |
| 🕐 **Heartbeat** | Always shows when it last checked, so you know it's running |
| ⚫ **Offline notice** | Posts an OFFLINE embed if the script stops or crashes |
| 🔒 **Secure** | Webhook URL lives in `.env` and is never committed |
| 📦 **Zero dependencies** | Pure Python 3.8+ standard library only |

---

## 📸 Preview

| Status | Embed |
|---|---|
| ✅ All operational | Green sidebar, "All components fully operational" |
| ⚠️ Minor outage | Yellow sidebar, affected components listed |
| 🔴 Major outage | Red sidebar, active incidents linked |
| ⚫ Monitor offline | Dark embed with stopped timestamp |

---

## 🚀 Setup

### 1. Clone the repo
```bash
git clone https://github.com/your-username/claude-status-monitor.git
cd claude-status-monitor
```

### 2. Create a Discord webhook
1. Open your Discord server
2. Go to **Server Settings → Integrations → Webhooks**
3. Click **New Webhook**, give it a name, choose a channel
4. Click **Copy Webhook URL**

> ⚠️ **Never share your webhook URL** — Discord will automatically revoke any URL that gets exposed publicly.

### 3. Configure `.env`
Create a `.env` file in the project folder:
```env
DISCORD_WEBHOOK=https://discord.com/api/webhooks/YOUR_ID/YOUR_TOKEN
```

### 4. Run
```bash
python3 main.py
```

Press `Ctrl+C` to stop — the Discord message will automatically update to show the monitor is offline.

---

## 📁 Project Structure

```
claude-status-monitor/
├── main.py            # Entry point — run this
├── config.py          # Loads .env, defines colours & constants
├── status_client.py   # Fetches the Anthropic status API
├── discord_client.py  # Builds embeds, handles POST & PATCH
├── state.py           # Persists status snapshot & message ID
├── .env               # Your webhook URL (git-ignored)
└── status_state.json  # Last known state (git-ignored)
```

---

## 📋 Requirements

- **Python 3.8+**
- No external packages — uses the standard library only

---

## 📄 License

MIT © [Ban](https://github.com/your-username)
