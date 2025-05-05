# 🧠 AI Support Triage
[![CI](https://github.com/JanovK/ai-support-triage/actions/workflows/ci.yml/badge.svg)](https://github.com/JanovK/ai-support-triage/actions/workflows/ci.yml)

Welcome to the official repository of **AI Support Triage** — a solo Capstone Project developed as part of the *Master of Science in Information Technology* at University of the People.

This platform leverages modern **Natural Language Processing (NLP)** and **MLOps** practices to **analyze**, **prioritize**, and **secure** multichannel support tickets (email, chat, JSON streams), enabling service teams to respond faster, reduce SLA violations, and limit data exposure risks.

> 🔗 **Live demo** (secured dashboard): [ai-support-triage.streamlit.app](https://ai-support-triage.streamlit.app)

> **Username**: `admin`  
> **Password**: `uTdY1qw^HRCXx0MW`

---

## 🚀 Project Objective

Modern support operations face three key challenges:
- Overwhelming ticket **volume** (email, chat, voice-to-text)
- Growing **velocity** of multichannel customer queries
- **Vulnerability** due to unmasked PII and inconsistent triage

**AI Support Triage** provides an intelligent mechanism to:
- 🔒 **Automatic PII masking**
- 🧠 **Semantic topic clustering**
- 🚨 **Hybrid urgency scoring (rules + sentiment)**
- ⚖️ **Queue prioritization (RL-ready)**
- 📊 **Interactive Streamlit dashboard**
- 🐳 **Dockerized deployment + CI/CD**

---

### 🔧 Core Modules

| Module                | Tech Stack                               | Description |
|----------------------|-------------------------------------------|-------------|
| Ingestion            | `FastAPI`, `asyncio`, `YAML`              | Load ticket streams from various formats |
| PII Masking          | `spaCy`, `regex`, `langdetect`           | Detect and redact sensitive data in text |
| Topic Clustering     | `sentence-transformers`, `HDBSCAN`        | Group requests by latent semantic themes |
| Urgency Scoring      | `transformers`, `custom rules`            | Identify tickets that need urgent action |
| Prioritization       | PPO-based engine (planned)                | Sort queue to minimize MTTR |
| Explainability       | `SHAP`, `LIME`, attention visualization   | Transparent, auditable decision-making |
| Dashboard            | `Streamlit`, `pandas`, `SHA256 login`        | View and filter tickets securely |
| Pipeline             | `run_pipeline.py`                            | Full E2E flow from ingest to scoring |
| CI/CD                | GitHub Actions                               | Auto-test and build validation |
| Docker               | `python:3.10-slim`                           | Portable, production-ready image |

---

## 🧪 Running Locally

```bash
# Clone the repo
git clone https://github.com/JanovK/ai-support-triage.git
cd ai-support-triage

# Set up environment
./setup.sh            # Linux/macOS
# or
setup.bat             # Windows

# Activate venv and run tests
source venv/bin/activate
pytest tests/

# Start ingestion module
python src/ingest.py --config configs/demo.yaml

```

---

## 🔁 Full Pipeline (CLI)

```bash
python src/run_pipeline.py --file data/sample_tickets.json

```
➡️ Generates: data/sample_tickets_anonymized_clustered_scored.json

---

---


# 📊 Dashboard & Deployment Guide

## 📊 Dashboard (local)

```bash
streamlit run src/dashboard.py
```

🔐 **Login required**  
Set credentials in `.env` or Streamlit Cloud secrets:

```env
DASHBOARD_USERNAME=admin
DASHBOARD_PASSWORD_HASH=<SHA256_HASH>
```

> Use SHA256 hash generated with:  
> `hashlib.sha256("your_password".encode()).hexdigest()`

---

## 🐳 Docker (Optional)

```bash
docker build -t ai-support-triage .
docker run -p 8501:8501 ai-support-triage
```

> Automatically runs the Streamlit dashboard

---

## 🌐 Deployment on Streamlit Cloud

1. Push to GitHub
2. Deploy from [streamlit.io/cloud](https://streamlit.io/cloud)
3. Main script: `src/dashboard.py`
4. Add secrets in UI:

```toml
DASHBOARD_USERNAME = "admin"
DASHBOARD_PASSWORD_HASH = "<SHA256_HASH>"
```

---

## ✅ Testing

```bash
# Run all unit & functional tests
PYTHONPATH=src pytest tests/
```

Includes tests for:
- PII masking
- Clustering
- Urgency scoring
- Full pipeline integration

---

## 📅 Capstone Roadmap (Recap)

| Week | Deliverables |
|------|--------------|
| ✅ Week 1 | SRS + skills audit |
| ✅ Week 2 | Ingestion + PII masking |
| ✅ Week 3 | Clustering + scoring |
| ✅ Week 4 | Dashboard + deploy + test coverage + Docker |

---


## 👨‍💻 About the Author

**Jean-François Kantke**  
Senior Software Developer | 🇨🇦 Canadian & 🇫🇷 French  
NLP & Cloud Architecture Enthusiast  
📍 Montreal, QC, Canada  | 🔗 [LinkedIn](https://www.linkedin.com/in/jeanfrancoiskantke)

---

## 📄 License

This project is licensed under the MIT License — see the LICENSE file for details.