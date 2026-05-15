# Installation Guide — Hermes Business OS

> **New here?** Start with the [README](../../README.md) for the big picture.

---

## Overview

Hermes Business OS (HBOS) is a **skill pack** for [Hermes Agent](https://github.com/NousResearch/hermes-agent). You must install Hermes Agent first, then add HBOS on top.

**Total setup time: ~15 minutes**

---

## Requirements

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| OS | macOS 12+, Ubuntu 20.04+, WSL2 | Latest macOS or Ubuntu LTS |
| RAM | 4 GB | 8 GB+ |
| Disk | 2 GB free | 5 GB+ |
| Python | 3.11 (installed by Hermes) | 3.11+ |
| Node.js | 18+ (for dashboard) | 20+ |
| AI Model | Any OpenAI-compatible API | OpenRouter (200+ models) |

---

## Step 1 — Install Hermes Agent (Required)

HBOS does not work without Hermes Agent. Install it first.

### One-line installer

```bash
curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash
```

This handles everything: Python 3.11, Node.js, dependencies, and the `hermes` command.

### Verify installation

```bash
source ~/.bashrc    # or: source ~/.zshrc
hermes --version    # Should print: hermes-agent v0.x.x
```

If something fails:
```bash
hermes doctor
```

> 📖 [Full Hermes Agent docs →](https://hermes-agent.nousresearch.com/docs/)

---

## Step 2 — Install HBOS

### Option A: Quick install (recommended)

```bash
git clone https://github.com/cuentadeservicio377-cell/hermes-business-os.git
cd hermes-business-os
bash scripts/install.sh
```

The install script will:
1. Check that Hermes Agent is installed
2. Copy HBOS skills to `~/.hermes/skills/`
3. Install Python dependencies (`pyyaml`, `google-api-python-client`, `weasyprint`, etc.)
4. Run a quick health check

### Option B: Manual install

```bash
git clone https://github.com/cuentadeservicio377-cell/hermes-business-os.git
cd hermes-business-os

# Copy skills
mkdir -p ~/.hermes/skills
cp -r skills/* ~/.hermes/skills/

# Install Python deps
pip install pyyaml google-api-python-client google-auth-httplib2 \
  google-auth-oauthlib weasyprint

# Verify
bash scripts/test.sh
```

### Option C: Docker

```bash
cd hermes-business-os
docker-compose -f docker/docker-compose.yml up --build
```

> **Note:** Docker mode runs the dashboard only. Hermes Agent itself must still be installed on your host or a separate container.

---

## Step 3 — Configure your business

```bash
hbos setup
```

The setup wizard runs in your terminal and asks:

```
? Company name: Mi Empresa
? Industry: [events | legal | consulting | retail | custom]
? Team size: 5
? Currency: MXN
? Activate departments: [x] Sales [x] Operations [x] Documents [x] Finance [x] HR
```

After completion:
- `config/empresa.yaml` is created
- Data files are generated in `data/`
- Industry catalog is loaded
- Sample data is seeded (optional)

### Manual configuration

If you prefer to configure by hand:

```bash
cp config/empresa.yaml.example config/empresa.yaml
# Edit config/empresa.yaml with your favorite editor
```

---

## Step 4 — Configure Telegram (recommended)

HBOS works best through Telegram. You need a bot token.

### Create a bot

1. Open Telegram and search for **@BotFather**
2. Send `/newbot`
3. Follow prompts: name your bot, choose a username
4. Copy the **token** (looks like `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`)

### Configure Hermes gateway

```bash
hermes gateway setup
```

Follow the prompts to paste your Telegram token.

### Start the gateway

```bash
hermes gateway start
```

Your bot is now live. Send `/start` on Telegram to begin.

> 💡 **Tip:** Use `hermes gateway start &` or `tmux` to keep it running in the background.

---

## Step 5 — Configure Google Workspace (optional but recommended)

Google Workspace sync lets HBOS:
- Save data to Google Sheets you control
- Create documents in Google Drive
- Use your existing Google Calendar

### 1. Create a Google Cloud project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project
3. Enable APIs: **Sheets API**, **Drive API**, **Docs API**, **Slides API**, **Calendar API**

### 2. Create a service account

1. Go to **IAM & Admin → Service Accounts**
2. Click **Create Service Account**
3. Name it: `hermes-business-os`
4. Grant roles: **Editor** (for Sheets/Drive access)
5. Create a key: **JSON** format
6. Download the JSON file

### 3. Move the key to HBOS

```bash
mv ~/Downloads/your-service-account.json config/google-service-account.json
```

### 4. Share your Sheets/Drive

1. Open the JSON file and copy the `client_email` (looks like `hermes@project-123.iam.gserviceaccount.com`)
2. Create a Google Sheet called **"Hermes Business OS — Master"**
3. Share the sheet with that email address (give **Editor** permission)
4. Do the same for your Google Drive folder

### 5. Activate in HBOS

Edit `config/empresa.yaml`:

```yaml
integraciones:
  google_workspace:
    activa: true
    drive_folder_id: ""        # Optional: paste your Drive folder ID
    sheets_master_id: ""       # Optional: paste your Sheet ID
```

---

## Step 6 — (Optional) Web Dashboard

```bash
cd dashboard
npm install
npm run dev
```

Open [http://localhost:3000](http://localhost:3000)

For production:
```bash
npm run build
npm start
```

---

## Verification

Run the full test suite:

```bash
bash scripts/test.sh
```

Expected output: **All tests passing**.

Check HBOS status:
```bash
hbos status
hbos doctor
```

---

## Troubleshooting

### "Hermes Agent not found"

Install Hermes first:
```bash
curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash
source ~/.bashrc
```

### "Python dependencies missing"

```bash
pip install --user pyyaml google-api-python-client \
  google-auth-httplib2 google-auth-oauthlib weasyprint
```

### "Skills not loading"

```bash
# Reinstall skills
hbos install

# Verify skill path
ls ~/.hermes/skills/hermes-*
```

### "Google Workspace not working"

1. Verify `config/google-service-account.json` exists
2. Verify you shared the Sheet/Drive with the service account email
3. Verify APIs are enabled in Google Cloud Console
4. Check logs: `hermes logs`

### "Gateway won't start"

```bash
# Check if another instance is running
ps aux | grep hermes

# Kill and restart
pkill -f hermes-gateway
hermes gateway start
```

---

## Next Steps

- [User Guide](USER-GUIDE.md) — Daily usage examples
- [Admin Guide](ADMIN-GUIDE.md) — Advanced configuration
- [API Reference](API.md) — Developer documentation

---

*For support, open an issue on GitHub or visit [wsc.lat](https://wsc.lat)*
