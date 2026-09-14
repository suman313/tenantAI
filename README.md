# 🏠 TenantAI — AI Maintenance Agent for Property Managers

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://python.org)
[![LangGraph](https://img.shields.io/badge/LangGraph-Agent-orange)](https://langchain.com/langgraph)
[![FastAPI](https://img.shields.io/badge/FastAPI-Backend-green)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React-18-61DAFB.svg)](https://react.dev)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**An AI agent that reads tenant maintenance emails, classifies issues, dispatches contractors via WhatsApp, and tracks everything in a real‑time dashboard.**

> Built to solve a problem validated by 9,300+ “I wish there was an app for this” posts on Reddit.

---

## 🎥 Demo

[![Demo Video](https://img.youtube.com/vi/YOUR_VIDEO_ID/0.jpg)](https://youtu.be/YzdHttviDoA)

*2‑minute walkthrough: email ingestion → LLM classification → WhatsApp dispatch → dashboard update.*

---

## 🧩 Overview

Property managers spend **10‑15 hours/week** manually triaging tenant emails, coordinating contractors, and tracking requests. TenantAI automates the entire flow end‑to‑end — from an unstructured email arriving in the inbox to a WhatsApp notification on a contractor’s phone.

It’s built as a **production‑grade AI agent** using LangGraph, FastAPI, React, and multiple external APIs, demonstrating real‑world AI engineering skills beyond simple prompt calling.

---

## ❓ Problem & Solution

| Problem                                                                                                    | Solution                                                                                                 |
| ---------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------- |
| Tenants send messy, unstructured emails (“water falling from ceiling, plz come urgent, key with neighbor”) | LLM‑powered classifier extracts issue type, urgency, unit number, access instructions, and tenant phone. |
| PM manually figures out which contractor to call                                                           | Intelligent dispatcher maps issue type to the right contractor (plumber, electrician, etc.).             |
| No audit trail of requests                                                                                 | Every interaction is saved to a database with email thread links and status tracking.                    |
| Contractors are notified slowly via phone calls                                                            | WhatsApp message is sent instantly with all job details.                                                 |
| PM has no central view of all requests                                                                     | React dashboard shows all requests, allows status updates, and links back to original emails.            |

---

## ✨ Features

- 🤖 **Autonomous AI agent** (LangGraph) – classifies, dispatches, notifies, replies, and marks emails as read.
- 🧠 **Custom LLM classification** – uses OpenRouter (Claude/GPT) with prompt engineering to extract structured data from free‑form text.
- 📧 **Gmail integration** – OAuth‑secured polling for new maintenance emails and threaded replies.
- 📲 **WhatsApp notifications** – Twilio sends job details to contractors.
- 🗄️ **Full audit trail** – SQLite (switchable to PostgreSQL) stores every request with email IDs, contractor info, and timestamps.
- 📊 **Real‑time dashboard** – React + FastAPI shows all requests, allows status updates, and links to Gmail.
- ⚡ **Error‑safe workflow** – If any step fails (e.g., Twilio down), the agent stops gracefully and logs the error.

---

## 🛠️ Tech Stack

| Layer            | Technologies                                   |
| ---------------- | ---------------------------------------------- |
| **AI / Agent**   | Python, LangGraph, LangChain, OpenRouter (LLM) |
| **Backend API**  | FastAPI, Uvicorn                               |
| **Frontend**     | React (Vite), Tailwind CSS, Axios              |
| **Integrations** | Gmail API, Twilio (WhatsApp), SQLite           |
| **DevOps**       | GitHub Codespaces, Docker‑ready                |

---

## 🧠 Architecture

```
┌───────────┐
│  TENANT   │
│  Email    │
└─────┬─────┘
      │
      ▼
┌──────────┐    ┌──────────────┐    ┌────────────┐    ┌────────────┐
│ 1. GMAIL │───▶│ 2. CLASSIFY  │───▶│ 3. DISPATCH │───▶│ 4. SAVE DB │
│   POLL   │    │  (OpenRouter) │    │ (contractor)│    │            │
└──────────┘    └──────────────┘    └────────────┘    └─────┬──────┘
                                                            │
                     ┌──────────────────────────────────────┘
                     ▼
              ┌─────────────┐
              │ 5. NOTIFY   │  WhatsApp → Contractor
              └──────┬──────┘
                     │
                     ▼
              ┌─────────────┐
              │ 6. REPLY    │  Email → Tenant (tracking #)
              └──────┬──────┘
                     │
                     ▼
              ┌─────────────┐
              │ 7. MARK READ│
              └──────┬──────┘
                     │
                     ▼
              ┌───────────────────────────────────┐
              │            DASHBOARD              │
              │  React + FastAPI                  │
              │  • View all requests              │
              │  • Update status                  │
              │  • Open original email in Gmail   │
              └───────────────────────────────────┘
```

The entire workflow is orchestrated by a **LangGraph StateGraph** with conditional error routing — no step proceeds if a previous one fails.

---

## ⚙️ How It Works (Step by Step)

1. **Poll Gmail** – Searches for unread emails containing “maintenance”, “leaking”, “repair”.
2. **Classify** – The email body is sent to an LLM (via OpenRouter) that returns structured JSON: issue type, urgency, unit, phone, access instructions.
3. **Dispatch** – A contractor directory (issue type → name + phone) selects the right person.
4. **Save** – A complete record is written to SQLite: email ID, tenant info, issue, contractor, status, timestamp.
5. **Notify** – A WhatsApp message is sent to the contractor with all details.
6. **Reply** – A confirmation email is threaded back to the tenant with a tracking number.
7. **Mark read** – The email is archived so it’s not processed again.
8. **Dashboard** – All requests are displayed in a React dashboard. The property manager can change status (received → in progress → completed) and click to open the original email in Gmail.

---

## 🚀 Setup & Running Locally

### Prerequisites
- Python 3.10+
- Node.js 18+
- Gmail API credentials (OAuth 2.0)
- OpenRouter API key (or Anthropic/DeepSeek)
- Twilio account (WhatsApp sandbox)

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/tenantAI.git
cd tenantAI
```

### 2. Set up environment variables
Create a `.env` file in the project root:
```
OPENROUTER_API_KEY=sk-or-v1-...
TWILIO_ACCOUNT_SID=AC...
TWILIO_AUTH_TOKEN=...
TWILIO_WHATSAPP_NUMBER=+14155238886
```

### 3. Backend
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
# Place your credentials.json (Gmail) in the root
python init_db.py           # create database tables
uvicorn backend.api.main:app --reload --port 8000
```

### 4. Frontend
```bash
cd frontend
npm install
npm run dev
```

### 5. Run the agent
```bash
python main.py   # processes one test email (or set up a scheduler for polling)
```

---

## 📊 Dashboard

![Dashboard Screenshot](screenshots/dashboard.png)

- **Request Cards** – Show issue type, unit, urgency, contractor, status.
- **Status Dropdown** – Update request status in real‑time.
- **Gmail Link** – Opens the original email thread in one click.

---


## 🔁 TenantAI vs No‑Code Platforms (Zapier, Rival.io)

|                                    | No‑Code | TenantAI |
| ---------------------------------- | :-----: | :------: |
| Understands unstructured emails    |    ❌    |    ✅     |
| Custom LLM prompt engineering      |    ❌    |    ✅     |
| Multi‑step agentic decisions       |    ❌    |    ✅     |
| Full code ownership & data privacy |    ❌    |    ✅     |
| Portfolio‑worthy engineering       |    ❌    |    ✅     |

No‑code tools can do “if email contains X → send Slack message”. TenantAI can **read** the email, **understand** it, **decide** what to do, and **act** — all autonomously.

---

## 🗺️ Future Enhancements

- [ ] FAQ auto‑reply (search lease docs to answer tenant questions)
- [ ] Compliance audit trail (timestamped logs for legal protection)
- [ ] Bulk tenant letters (write a short note → AI formats and emails all tenants)
- [ ] WebSocket real‑time dashboard updates
- [ ] Multi‑property support with user authentication

---

## 📄 License

MIT © Suman Modak

---

## 📬 Contact

**Suman Modak**  
[GitHub](https://github.com/suman313) | [LinkedIn](https://www.linkedin.com/in/modak-suman/)  
Email: sumanmodak616@gmail.com
