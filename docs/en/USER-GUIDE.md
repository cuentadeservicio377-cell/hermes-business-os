# User Guide — Hermes Business OS

This guide shows you how to use HBOS day-to-day. No technical knowledge required — just talk to Hermes like you talk to a person.

---

## First Conversation

Open Telegram and message your bot:

```
/start
```

Hermes will greet you and begin the business onboarding if you haven't completed `hbos setup` yet.

---

## Daily Workflow

### Morning check-in

```
You: Good morning, what do I have today?

Hermes: Good morning! Here's your business snapshot:
  📋 Tasks pending: 3
  💰 Payments due: 2
  📊 Projects in progress: 2

Pending tasks:
  1. Confirm venue for Martínez wedding (due today)
  2. Send quote to González (due tomorrow)
  3. Register López project payment (overdue 2 days)

Want details on any of these?
```

### Sales — Register a client

```
You: I got a new client. Maria Gonzalez, wants a quinceañera for 80 people in February.

Hermes: Great! Maria Gonzalez registered as a prospect. 
  ID: CLI-001
  Service: Quinceañera
  Guests: 80
  Month: February

Shall I generate a quote?

You: Yes, intermediate package.

Hermes: Generating quote... Done!
  Items:
    - Intermediate package (EVT-INT): $35,000 x 1 = $35,000
  Subtotal: $35,000
  IVA (16%): $5,600
  Total: $40,600 MXN

Want me to create the PDF and send it to your Drive?
```

### Operations — Create a project

```
You: Create project "Quinceañera Maria" for February 15th.

Hermes: Project created!
  ID: PROJ-001
  Name: Quinceañera Maria
  Delivery: 2026-02-15
  Status: Planning

Should I create the checklist?

You: Yes, events template.

Hermes: Checklist created with 3 phases:
  📋 Pre-event (4 tasks)
  📋 Event day (4 tasks)
  📋 Post-event (4 tasks)

First task: "Confirm date and venue" — want to assign it?
```

### Finance — Check money

```
You: How much did we invoice this month?

Hermes: May 2026 financial summary:
  💵 Income: $127,500 MXN
  💸 Expenses: $45,200 MXN
  📈 Margin: $82,300 (65%)

Pending collections:
  - García project: $12,000 (5 days overdue)
  - Díaz project: $8,500 (3 days overdue)

Want me to send payment reminders?
```

### Documents — Generate a contract

```
You: Generate service contract for Maria Gonzalez.

Hermes: Document generated!
  Template: Eventos / Service Contract
  Client: Maria Gonzalez
  Service: Quinceañera package
  Amount: $40,600 MXN

Saved to: data/documents/CONTRATO-CLI-001.pdf
Also uploaded to Google Drive ✅

Preview: [link]
```

### HR — Register attendance

```
You: Juan worked 8 hours on the Martinez project today.

Hermes: Attendance registered!
  Employee: Juan Perez (EMP-001)
  Project: Martinez Wedding (PROJ-002)
  Date: 2026-05-15
  Hours: 8
  Type: Work

Juan has 32 hours this week. At $800/day, payroll so far: $3,200 MXN.
```

---

## Commands Reference

You don't need exact commands — Hermes understands natural language. But here are patterns that work reliably:

### Sales

| What you say | What Hermes does |
|-------------|-----------------|
| "Register client [name]" | Creates client record |
| "Quote [service] for [client]" | Generates quote with catalog prices |
| "What's my pipeline?" | Shows sales pipeline |
| "Follow up with [client]" | Schedules follow-up reminder |
| "How many leads this month?" | Shows lead summary |

### Operations

| What you say | What Hermes does |
|-------------|-----------------|
| "Create project [name]" | Creates project with ID |
| "What tasks are pending?" | Lists overdue and upcoming tasks |
| "Mark [task] as done" | Completes task, updates progress |
| "Who's working on [project]?" | Shows assigned team |
| "Create checklist for [project]" | Generates industry checklist |

### Finance

| What you say | What Hermes does |
|-------------|-----------------|
| "How much did we invoice?" | Monthly report |
| "Register payment from [client]" | Records payment transaction |
| "What's overdue?" | Lists overdue payments |
| "Budget for [project]" | Shows or creates budget |
| "Cash flow" | 6-month cash flow chart |

### Documents

| What you say | What Hermes does |
|-------------|-----------------|
| "Generate quote for [client]" | PDF quote |
| "Generate contract for [client]" | PDF contract |
| "What templates do we have?" | Lists available templates |
| "Generate [document]" | Creates document with variables |

---

## Tips for Best Results

1. **Use client names consistently** — Hermes remembers them. "Maria G" works if you registered her that way.

2. **Be specific about dates** — "February 15th" is better than "next month."

3. **You can send voice messages** — Hermes transcribes audio on Telegram.

4. **Mention project IDs when context is unclear** — "Update PROJ-003" instead of "Update the wedding project" if you have multiple weddings.

5. **Hermes learns your business** — The more you use it, the better it understands your vocabulary, clients, and processes.

6. **Check the dashboard for visual overviews** — While chat is the primary interface, the web dashboard is great for visualizing pipelines and project timelines.

---

## Industry Examples

### Events (Weddings, Quinceañeras, Parties)

```
"Register a new client: Laura Vargas, wedding for 120 people, June 20th"
"Quote wedding for 120, premium package"
"Create project Wedding Laura Vargas"
"Generate contract for Laura Vargas"
"What's the event checklist?"
"How much do we have in deposits?"
```

### Legal Services

```
"Register client: ABC Corp, needs contract review"
"Quote contract review for ABC Corp"
"Create project Contract Review ABC"
"Generate retainer agreement for ABC Corp"
"How many active cases?"
"Billable hours this month"
```

### Consulting

```
"Register client: TechStart, marketing consulting"
"Quote 3-month consulting for TechStart"
"Create project Marketing Consulting TechStart"
"Generate project proposal"
"What's the project status?"
```

### Retail

```
"Register supplier: Distribuidora del Sur"
"What's our inventory status?"
"Create purchase order for 50 units"
"Sales report this week"
"Who owes us money?"
```

---

## Common Mistakes

❌ **"Do everything"** — Hermes works best with one request at a time.

✅ **"Create project X. Then quote for client Y."**

❌ **Vague references** — "That client from last week"

✅ **"The client we registered on May 10th"** or use the client ID

❌ **Assuming Hermes knows context** — If you switch topics, re-state the project/client name.

---

*Questions? Check the [Admin Guide](ADMIN-GUIDE.md) or open an issue on GitHub.*
