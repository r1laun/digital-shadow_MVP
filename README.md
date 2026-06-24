[README.md](https://github.com/user-attachments/files/29283995/README.md)
# digital-shadow_MVP

**OSINT Threat Monitoring System for Kazakhstan**

AI-powered intelligence platform for detecting illegal activity across open internet and Telegram sources.

![Python](https://img.shields.io/badge/Python-3.11-blue?style=flat-square)
![FastAPI](https://img.shields.io/badge/FastAPI-0.110-green?style=flat-square)
![Groq](https://img.shields.io/badge/AI-Groq%20LLaMA3-purple?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-gray?style=flat-square)

---

## Features

- **OSINT Search** — scan Telegram channels and public sources
- **AI Analysis** — LLaMA3-70B classifies threats via Groq API
- **Risk Scoring** — 0–100 threat index with category detection
- **History** — SQLite log of all analyst queries
- **Cybersecurity UI** — dark dashboard interface

## Threat Categories

| Category | Description |
|---|---|
| наркотики | Drug trade signals |
| вейпы/алкоголь | Contraband vapes & alcohol |
| дропы | Money mule / drop schemes |
| утечка_БД | Kazakhstan database leaks |
| крипто-мошенничество | Suspicious crypto wallets |
| нет_угрозы | No threat detected |

---

## Quick Start

```bash
git clone https://github.com/YOUR_USERNAME/digital-shadow
cd digital-shadow

pip install -r requirements.txt

cp .env.example .env
# Add your API keys to .env

python main.py
```

Open `http://localhost:8000`

## Environment Variables

```env
GROQ_API_KEY=your_groq_api_key        # from console.groq.com (free)
TELEGRAM_API_ID=your_telegram_api_id  # from my.telegram.org (optional)
TELEGRAM_API_HASH=your_telegram_hash  # from my.telegram.org (optional)
```

> Without Telegram credentials the app runs in **demo mode** with mock data.

---

## Stack

- **Backend** — FastAPI + Uvicorn
- **AI** — Groq API (LLaMA3-70B)
- **Data** — Telethon (Telegram), SQLite
- **Frontend** — Jinja2 + Vanilla HTML/CSS

---

## Project Structure

```
digital-shadow/
├── main.py          # FastAPI app & routes
├── analyzer.py      # Groq AI threat analysis
├── search.py        # Telegram search via Telethon
├── database.py      # SQLite history
├── templates/
│   └── index.html   # Cybersecurity dashboard UI
├── vercel.json      # Vercel deployment config
└── requirements.txt
```

---

*Built for AFM Hackathon 2026 — Digital Shadow LarpGroup team*
