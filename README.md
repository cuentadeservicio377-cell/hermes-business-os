<div align="center">

# Hermes Business OS

### **The AI Operating System for Small Business in Latin America**

[![Powered by Hermes Agent](https://img.shields.io/badge/Powered%20by-Hermes%20Agent-6366f1?style=flat-square&logo=data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCI+PHBhdGggZD0iTTEyIDJDNi40NzcgMiAyIDYuNDc3IDIgMTJzNC40NzcgMTAgMTAgMTAgMTAtNC40NzcgMTAtMTBTMTcuNTIzIDIgMTIgMnptMCAxOGMtNC40MTggMC04LTMuNTgyLTgtOHMzLjU4Mi04IDgtOCA4IDMuNTgyIDggOC0zLjU4MiA4LTggOHptLTEtMTN2N2w1LjUgMy41TDE3LjUgMTRsLTQuNS0yLjVWN2wtMSAxeiIgZmlsbD0id2hpdGUiLz48L3N2Zz4=)](https://github.com/NousResearch/hermes-agent)
[![Tests](https://img.shields.io/badge/Tests-73%2F73%20passing-22c55e?style=flat-square)](scripts/test.sh)
[![License: MIT](https://img.shields.io/badge/License-MIT-f59e0b?style=flat-square)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.11%2B-3776ab?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![Next.js](https://img.shields.io/badge/Next.js-15-000000?style=flat-square&logo=next.js&logoColor=white)](https://nextjs.org)

**[📄 Español](README.es.md)** · **[📖 Docs](docs/)** · **[🔬 Research Paper (EN)](docs/RESEARCH-PAPER.en.md)** · **[🔬 Research Paper (ES)](docs/RESEARCH-PAPER.md)** · **[🚀 Quick Start](#quick-start)**

</div>

---

## What is this?

**Hermes Business OS** is a **distribution of native skills** for [Hermes Agent](https://github.com/NousResearch/hermes-agent) (by Nous Research) that transforms the AI agent into the **operating system of your small business**.

It is **not** a separate app. It is **not** a backend server. It is a set of business intelligence skills that plug directly into Hermes Agent — the same way a theme turns a phone into something personal, HBOS turns Hermes into your business partner.

<div align="center">

```
┌────────────────────────────────────────────────────────────┐
│  You send a message on WhatsApp or Telegram                │
│       ↓                                                    │
│  Hermes Agent (Nous Research) understands your intent      │
│       ↓                                                    │
│  HBOS routes to the right business skill                   │
│       ↓                                                    │
│  Your data is saved · Documents are generated · Follow-ups │
│     are scheduled · Reports are ready                      │
└────────────────────────────────────────────────────────────┘
```

</div>

### Three things that make it different

| 🗣️ **Talk, don't click** | 📱 **WhatsApp is your dashboard** | 💰 **Zero license cost** |
|:---|:---|:---|
| No menus. No training. You talk to your business like you talk to a partner. "How much did we invoice this month?" | 70% of Latin American small businesses sell through WhatsApp. HBOS lives where you already are. | Open source (MIT). No per-user fees. No monthly subscriptions. You only pay for the AI model you choose. |

---

## Who is this for?

This was built for the **99.5%** of Latin American businesses that are small — the ones that generate **60-67% of formal employment** but contribute only **~25% of GDP** because they are trapped doing administration by hand.

- ✅ Business owners with 1–20 employees
- ✅ Businesses with repetitive processes (events, legal, retail, consulting)
- ✅ People who are slaves to their own administration
- ✅ Anyone who wants to stop losing clients due to lack of follow-up
- ✅ Teams that sell through WhatsApp and track finances in Excel

> **Not for:** Entrepreneurs learning their industry, or companies looking for a ready-made platform with zero customization.

---

## A day with Hermes

> **You:** "Good morning, what do I have today?"  
> **Hermes:** "You have 3 pending tasks: confirm the venue for the Martínez wedding, send the quote to González, and register the López project payment. The López payment is due tomorrow. Want me to send a reminder?"
>
> **You:** "Register a new client: Carlos Ruiz, wants a quinceañera for 80 people in February."  
> **Hermes:** "Done. Carlos Ruiz registered as a prospect. Generating intermediate package quote... Total: $35,000 MXN. Send it?"
>
> **You:** "How is the Martínez wedding going?"  
> **Hermes:** "Progress: 65%. Tasks completed: 8/12. Pending: confirm catering (due today) and sound check (tomorrow). Mark catering as in progress?"
>
> **You:** "How much did we invoice this month?"  
> **Hermes:** "$127,500 MXN collected, $45,000 pending. You have 2 overdue payments: García ($12,000, 5 days) and Díaz ($8,500, 3 days). Send reminders?"

**That is the entire interface.** One chat. Zero clicks.

---

## What you get

### 6 business skills

| Skill | What it does | For whom |
|-------|-------------|----------|
| **Sales** (`hermes-ventas`) | CRM, automatic quotes, pipeline tracking | Anyone who sells services |
| **Operations** (`hermes-operaciones`) | Projects, tasks, checklists, deadlines | Anyone who delivers projects |
| **Documents** (`hermes-documentos`) | Professional PDFs, contracts, proposals | Anyone who sends quotes or contracts |
| **Finance** (`hermes-finanzas`) | Budgets, payments, cash flow, overdue alerts | Anyone who handles money |
| **HR** (`hermes-rrhh`) | Team roster, attendance, payroll by project | Anyone who hires per-event staff |
| **Core** (`hermes-business-core`) | Company config, routing, Google Workspace | Everyone |

### Key features

- 🧠 **Persistent memory** — Hermes remembers every client, every project, every preference
- 📄 **Automatic documents** — Quotes, contracts, reports generated via chat command
- 📊 **Google Workspace sync** — Data lives in Sheets you control; documents in Drive
- 🎨 **Web dashboard** — Next.js 15 dashboard for visual overview (optional)
- 🏭 **Industry templates** — Pre-configured for events, legal, consulting, retail
- 🔧 **Conversational onboarding** — "Tell me about your business" — done in 15 minutes

---

## Architecture

```
Hermes Agent (official Nous Research — installed separately)
├── AI Core, Memory, Gateway, CLI
├── Telegram / WhatsApp / Discord / Slack integration
└── Native Skills System (SKILL.md + Python tools)
    └── HERMES BUSINESS OS (this repo)
        ├── hermes-business-core/     ← Config, intent routing, Google Workspace
        ├── hermes-ventas/            ← CRM, quote calculator, pipeline
        ├── hermes-operaciones/       ← Projects, tasks, checklists
        ├── hermes-documentos/        ← Kami v3 PDF engine, templates
        ├── hermes-finanzas/          ← Budgets, payments, reports
        └── hermes-rrhh/              ← Teams, attendance, payroll
```

**Critical design rule:** HBOS is NOT a separate backend. It is NOT a fork of Hermes. It is native Hermes skills + Python tools. This means you get upstream updates from Nous Research automatically — no merge hell.

---

## Quick Start

### Prerequisites

- **macOS**, **Linux**, or **WSL2** (Windows)
- **Hermes Agent** installed (see Step 1)
- A **Telegram bot token** (free via [@BotFather](https://t.me/BotFather))
- *(Optional)* **Google Workspace** account for Sheets/Drive sync

### Step 1 — Install Hermes Agent (required prerequisite)

HBOS is a skill pack for Hermes Agent. You must install Hermes first.

```bash
# One-line installer (handles Python 3.11, Node.js, all dependencies)
curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash

# Reload your shell
source ~/.bashrc   # or: source ~/.zshrc

# Verify
hermes --version
```

> 📖 [Full Hermes Agent documentation →](https://hermes-agent.nousresearch.com/docs/)

### Step 2 — Install HBOS

```bash
# Clone this repository
git clone https://github.com/cuentadeservicio377-cell/hermes-business-os.git

# Install HBOS skills into Hermes
cd hermes-business-os
bash scripts/install.sh

# Or manually copy skills to Hermes skills directory
cp -r skills/* ~/.hermes/skills/
```

### Step 3 — Configure your business

```bash
# Run the conversational setup wizard
hbos setup
```

The wizard will ask:
- Your company name
- Industry (events, legal, consulting, retail, or custom)
- Team size
- Currency
- Which departments to activate

It then generates `config/empresa.yaml` and sets up your data files automatically.

### Step 4 — Start the gateway

```bash
# Configure Telegram (one-time)
hermes gateway setup

# Start the gateway (Hermes is now live on Telegram)
hermes gateway start
```

Open Telegram and send `/start` to your bot. Hermes will greet you and begin the business onboarding.

### Step 5 — (Optional) Web dashboard

```bash
cd dashboard
npm install
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) for a visual overview.

---

## Installation methods

| Method | When to use | Command |
|--------|-------------|---------|
| **Quick install** | First time, clean system | `bash scripts/install.sh` |
| **Manual install** | Developers, customization | Copy `skills/` to `~/.hermes/skills/` |
| **Docker** | Server deployment | `docker-compose -f docker/docker-compose.yml up` |

---

## Documentation

| Document | Description |
|----------|-------------|
| [📖 Installation Guide](docs/en/INSTALL.md) | Detailed setup, troubleshooting, Google Workspace config |
| [👤 User Guide](docs/en/USER-GUIDE.md) | Daily usage examples by department |
| [⚙️ Admin Guide](docs/en/ADMIN-GUIDE.md) | Advanced configuration, backup, security |
| [🔌 API Reference](docs/en/API.md) | Python tool API for developers |
| [📄 Research Paper](docs/RESEARCH-PAPER.md) | Why this exists: digital inclusion in Latin America |
| [📝 Changelog](CHANGELOG.md) | Version history |
| [🤝 Contributing](CONTRIBUTING.md) | How to add skills, report issues, submit PRs |

---

## Why we built this

> Latin America does not need more entrepreneurs. It already has them — **99.5%** of its economy is made of them.
>
> What it needs is **infrastructure**. The same infrastructure that large corporations have had for decades: systems that let them know who owes them money, which projects are behind schedule, how much each service costs, and what opportunities they are missing.
>
> Existing business software is too expensive, too complex, and too foreign. A Mexican small business owner should not need to learn English, hire an IT consultant, or pay $100/user/month to manage 5 employees.
>
> **Hermes Business OS is not the solution. It is proof that the solution is possible.**

Read the full research: **[Digital Inclusion in Latin America](docs/RESEARCH-PAPER.md)**

---

## Tech Stack

| Layer | Technology |
|-------|------------|
| **Agent Core** | [Hermes Agent](https://github.com/NousResearch/hermes-agent) (Python, MIT) |
| **Skills** | Native SKILL.md + Python tools |
| **Dashboard** | Next.js 15 + React 19 + TypeScript + Tailwind CSS |
| **Documents** | Python + WeasyPrint (Kami v3) |
| **Data** | Google Sheets + local JSON |
| **Communication** | Telegram (primary) + WhatsApp + Dashboard |

---

## Contributing

We welcome contributions. See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

**Priority areas:**
- 🏭 More industry templates (healthcare, construction, agriculture)
- 🌍 Translations (Portuguese for Brazil)
- 📱 Mobile dashboard improvements
- 🔗 Payment gateway integrations
- 🗣️ Voice memo transcription

---

## Credits

- **[Hermes Agent](https://github.com/NousResearch/hermes-agent)** — Core framework by [Nous Research](https://nousresearch.com)
- **[WS Capital AI Lab](https://wsc.lat)** — Business skills adaptation and research
- **Real businesses** — Paola Meneses Decoración, Willow Narváez Legal, and more

---

## License

MIT License — Free to use, modify, and distribute.

---

<div align="center">

**The human thinks. Hermes executes. The human reviews. Hermes learns.**

_Made with ❤️ in Latin America for the 99.5%_

[⬆ Back to top](#hermes-business-os)

</div>
