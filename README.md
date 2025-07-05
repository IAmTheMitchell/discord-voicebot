# VoiceBot

VoiceBot is a lightweight Discord bot that posts a message in the first text channel it can write to whenever someone joins a voice channel. Idea and code originally from/heavily inspired by [Dan Petrolito's article](https://blog.danpetrolito.xyz/i-built-something-that-changed-my-friend-gro-social-fabric/).

---

## ✨ Features

| Feature | Details |
|---------|---------|
| Voice‑join announcements | Sends one of several random phrases (e.g., *“Mitchell jumped into General”*) whenever a member joins a voice channel. |
| Auto‑delete | Messages disappear after 5 minutes to keep channels tidy. |
| Private by default | Designed to run only on **your** server (toggleable in Discord Dev Portal). |
| Zero database required | Fully functional without a database (hooks included if you want to log joins). |
| Runs anywhere | Tested on Ubuntu 22.04/24.04 in an LXC container on Proxmox, but any system with Python ≥ 3.11 works. |

---

## 📝 Setup Guide

### 1 ‒ Create & Configure the Bot in Discord

1. **Open the Developer Portal:** <https://discord.com/developers/applications>  
2. **New Application** → give it a name (e.g. *VoiceBot*).  
3. **Installation → Install Link → *None***
3. **Bot → Add Bot → Yes, do it!**  
4. **Copy the Token** — you’ll need this for the `.env` file.  
5. **Privileged Gateway Intents:** toggle **Server Members Intent** **ON**.  
6. **Public Bot:** *OFF* (keeps your bot private).  
7. **OAuth2 → URL Generator**  
   - Scopes: **bot**  
   - Bot Permissions: **View Channels**, **Send Messages**, **Embed Links**  
   Copy the generated URL, visit it, and invite the bot to your server.

### 2 ‒ Install Python & uv

```bash
# Ubuntu example (Python 3.12 shown; adjust if you have 3.11/3.13):
sudo apt update && sudo apt install -y python3.12 python3.12-venv curl git

# Install uv (one‑liner)
curl -Ls https://astral.sh/uv/install.sh | sh
```

> **Why uv?** It’s a drop‑in replacement for `pip`/`venv` that installs dependencies in lightning‑fast Rust.

### 3 ‒ Install and Run

```bash
uv venv .venv
source .venv/bin/activate
uv pip install voicebot  # installs discord.py & python‑dotenv

# Create .env with your secret token
echo "DISCORD_TOKEN=YOUR-TOKEN-HERE" > .env

voicebot                 # launch!
```

### 4 ‒ Running 24 × 7 with systemd (Ubuntu/Debian)

> Replace paths & usernames to taste. The example assumes the repo is cloned to **/opt/voicebot** and a dedicated user named **voicebot** exists.

```bash
# 4.1  Create service user (optional but recommended)
sudo useradd -r -m -s /usr/sbin/nologin voicebot

# 4.2  Move code & create a persistent venv (or keep it in your home directory)
sudo mkdir -p /opt/voicebot
cd /opt/voicebot
sudo uv venv .venv
sudo ./.venv/bin/uv pip install voicebot

# 4.3  Store token in /opt/voicebot/.env (root‑only readable)
sudo nano /opt/voicebot/.env
#   DISCORD_TOKEN=PASTE-TOKEN-HERE
sudo chown voicebot:voicebot /opt/voicebot/.env
sudo chmod 600 /opt/voicebot/.env

# 4.4  Create the systemd unit
sudo tee /etc/systemd/system/voicebot.service > /dev/null <<EOF
[Unit]
Description=VoiceBot — Discord voice‑join announcer
after=network-online.target
wants=network-online.target

[Service]
Type=simple
User=voicebot
WorkingDirectory=/opt/voicebot
EnvironmentFile=/opt/voicebot/.env
ExecStart=/opt/voicebot/.venv/bin/voicebot
Restart=on-failure
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# 4.5  Fire it up
sudo systemctl daemon-reload
sudo systemctl enable --now voicebot
sudo journalctl -u voicebot -f   # live logs
```

### 5 ‒ Updating

```bash
sudo -iu voicebot
cd /opt/voicebot
git pull
source .venv/bin/activate
uv pip install voicebot --upgrade
exit
sudo systemctl restart voicebot
```

---

## 🧪 Development & Testing

| Task | Command |
|------|---------|
| Add a new dependency | `uv add PACKAGE_NAME` |
| Run unit tests (coming soon) | `uv pip install pytest && pytest` |
| Lint (optional) | `uv pip install ruff && ruff check .` |

Commit messages follow [Conventional Commits](https://www.conventionalcommits.org).

---

## 🛠 Troubleshooting

| Symptom | Fix |
|---------|-----|
| *Bot prints “TOKEN not set” and exits* | Ensure `.env` exists and `DISCORD_TOKEN` is correct. |
| *No message appears when someone joins voice* | 1) Verify the bot has **View Channels** & **Send Messages** perms in at least one text channel. 2) Make sure **Server Members Intent** is enabled and the bot was restarted afterward. |
| *systemd service keeps restarting* | `sudo journalctl -u voicebot -xe` for detailed logs. Most issues are missing token or bad Python path. |

---

## ❤️ Contributing

1. Fork → Branch → PR.  
2. Follow the commit style.  
3. All code must pass `pytest` and `ruff`.  
