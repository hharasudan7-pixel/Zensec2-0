# ZentraSec — AI-Powered Cybersecurity Incident Response & Threat Intelligence Platform

ZentraSec is an intelligent security operations platform built for small organizations, colleges, startups, and institutions that generate large volumes of security event data but lack a dedicated 24/7 security team. It continuously analyzes security events, detects abnormal behavior, correlates related events into a single incident, assigns a risk score, and provides an AI-assisted investigation and response workflow.

Built in a one-day hackathon (DevJams'26).

---

## The Problem

Small organizations generate large amounts of security data from login systems, servers, endpoints, networks, and applications — but often lack the staff to continuously monitor it. Suspicious activity like credential attacks, privilege abuse, malware behavior, and data exfiltration can go unnoticed or take too long to investigate.

*Example — instead of treating these as five unrelated events:*


50 failed logins → successful login → unusual IP → privilege escalation → large file download


ZentraSec identifies them as a single correlated incident:


🚨 Potential Account Compromise — Risk Score: 91/100
Evidence: Brute-force activity, then login from an unusual location, then privilege escalation.
Recommended action: Restrict the account, revoke sessions, verify MFA, investigate the downloaded file.


---

## Features

- 🔐 Real-time security event monitoring
- 🤖 AI-based anomaly detection (heuristic + Isolation Forest)
- 🕵️ Attack-pattern detection
- 📊 Threat/risk scoring
- 🔗 Event correlation — links related events into one incident
- 🚨 Automated incident alerts
- 🧠 *AI Incident Copilot* — a chat assistant that explains what happened, why it's suspicious, and what to do about it, with MITRE ATT&CK references
- 📋 Automated incident summaries
- 🌐 Attack timeline / security flow mapping
- 🔧 Suggested and executable response actions (isolate host, suspend account, etc.)
- 📈 Security analytics dashboard

---

## Architecture


Security Logs / Application Events / Network Data
                    ↓
              Data Collector
                    ↓
          Event Normalization
                    ↓
       ┌────────────┴────────────┐
       ↓                         ↓
Anomaly Detection          Rule Engine
       ↓                         ↓
       └────────────┬────────────┘
                    ↓
             Event Correlation
                    ↓
             Risk Scoring Engine
                    ↓
          AI Incident Copilot
                    ↓
        ┌───────────┴───────────┐
        ↓                       ↓
 Security Dashboard       Response Workflow


---

## Tech Stack

| Layer | Tools |
|---|---|
| Frontend | Next.js (React), Tailwind CSS |
| Backend | Python + FastAPI |
| AI / ML | Google Gemini (gemini-3.6-flash) for the Copilot; scikit-learn Isolation Forest for anomaly detection, with a heuristic fallback |
| Database | SQLite (dev) — PostgreSQL / Elasticsearch recommended for production log storage |
| Testing | pytest, pytest-asyncio, httpx |
| Deployment | Docker-ready; Uvicorn ASGI server |

---

## Project Structure


zensecai/
├── backend/
│   ├── main.py                     # FastAPI app, routes, request logging middleware
│   ├── schemas.py                  # Pydantic request/response models
│   ├── services/
│   │   ├── copilot.py              # AI Incident Copilot (Gemini integration + fallback)
│   │   ├── anomaly_detection.py    # Risk scoring / anomaly classification
│   │   └── correlation.py          # Event correlation logic
│   ├── tests/                      # pytest suite (backend + copilot + response actions)
│   └── requirements.txt
└── frontend/
    ├── src/app/
    │   ├── incidents/page.tsx      # Incident list & filtering
    │   ├── analytics/page.tsx      # Security analytics dashboard
    │   └── timeline/page.tsx       # Attack timeline / flow mapping
    └── src/components/dashboard/
        ├── CopilotPanel.tsx        # AI Copilot chat widget
        └── ResponseDrawer.tsx      # Response action execution panel


---

## Getting Started

### Prerequisites

- Python 3.10+
- Node.js 18+
- A Google Gemini API key ([aistudio.google.com](https://aistudio.google.com))

### Backend Setup

bash
cd zensecai/backend
pip install -r requirements.txt


Create a .env file in backend/:


GOOGLE_API_KEY=your_gemini_api_key_here


Run the backend:

bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000


### Frontend Setup

bash
cd zensecai/frontend
npm install
npm run dev


The dashboard will be available at http://localhost:3000.

---

## Running Tests

bash
cd zensecai/backend
python -m pytest tests/ -v


The suite covers the Copilot endpoint (happy path, validation errors, timeouts, rate limits, fallback responses), anomaly detection scoring, and response-action execution — 40+ tests, with two ML-path tests that require scikit-learn to be installed.

---

## AI Incident Copilot — Reliability Notes

The Copilot is designed to degrade gracefully rather than fail visibly during live use:

- *Timeouts*: The backend allows up to 25 seconds for a Gemini response (the frontend waits 28s, giving the backend priority to report a specific error first).
- *Rate limiting*: Gemini 429 / quota errors are detected and surfaced with a clear Retry-After header instead of hanging.
- *Fallback summaries*: If Gemini is unavailable, slow, or rate-limited, the Copilot automatically generates a structured incident summary directly from the incident's own data (risk score, evidence, detected attack pattern) instead of showing an error. These responses are clearly labeled [Quick Summary — AI analysis unavailable].
- *Bounded history*: Conversation history sent to Gemini is capped (MAX_HISTORY_TURNS, MAX_PROMPT_CHARS) to keep prompts fast and predictable.

---

## Security Notes

- API keys are read from environment variables only — never hardcoded, never logged.
- User question text is logged at DEBUG level only; incident IDs (not full payloads) are logged at INFO level, to avoid leaking sensitive incident details into log aggregators.
- CORS is restricted to explicit origins (localhost:3000 / 127.0.0.1:3000) rather than a wildcard.

---

## Accessibility

- All interactive controls (send button, filters, search, close buttons) have accessible labels.
- The incident list supports full keyboard navigation (Tab, Enter/Space, visible focus ring).
- The chat message log uses role="log" aria-live="polite", and the typing indicator is announced to screen readers via role="status".

---

## Known Limitations

- Isolation Forest–based anomaly scoring requires scikit-learn; without it, the system falls back to a heuristic scoring method automatically.
- Gemini free-tier API keys are subject to per-minute rate limits — for sustained testing or demos, pace requests a few seconds apart, or use a key with a paid tier.

---

## MITRE ATT&CK Alignment

The AI Incident Copilot references relevant MITRE ATT&CK techniques when explaining incidents (e.g. *T1078 — Valid Accounts* for credential-based compromise scenarios), grounding its explanations in an established threat-modeling framework rather than generic language.

---

## License

Built for hackathon purposes (DevJams'26). Add your preferred license here before public/production use.
