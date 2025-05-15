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
1. **Volume** — overwhelming numbers of tickets (email, chat, voice‑to‑text)
2. **Velocity** — growing speed and diversity of multichannel queries
3. **Vulnerability** — unmasked PII and inconsistent triage

**AI Support Triage** provides an intelligent mechanism to:
- 🔒 **Automatic PII masking**
- 🧠 **Semantic topic clustering**
- 🚨 **Hybrid urgency scoring (rules + sentiment)**
- ⚖️ **Queue prioritization (RL-ready)**
- 📊 **Interactive Streamlit dashboard**
- 🐳 **Dockerized deployment + CI/CD**

---

### 🔧 Core Modules

| Module                | Tech                 | Description                              |
|-----------------------|----------------------|------------------------------------------|
| Ingestion             | Python scripts       | Load JSON/CSV tickets via CLI           |
| PII Masking           | `spaCy`, `regex`     | Redact email, name, phone, address, etc. |
| Topic Clustering      | `sentence-transformers`, `HDBSCAN` | Cluster by intent         |
| Urgency Scoring       | `transformers`, rules| Sentiment + rule-based severity score    |
| API Service           | `FastAPI`, `Uvicorn` | Expose `/analyze-ticket` endpoint        |
| Dashboard             | `Streamlit`          | Filters, metrics, SHA256‑auth login      |
| Pipeline              | `run_pipeline.py`    | ingest → mask → cluster → score → save   |
| CI/CD                 | GitHub Actions       | Automated tests & build                  |
| Containerization      | `Docker`, `docker-compose` | API & dashboard services      |

---

### 📡 REST API

### Endpoints

#### `GET /health`

Returns:

```json
{ "status": "ok" }
```

#### `POST /analyze-ticket`

**Headers**

```
Authorization: Bearer <API_KEY>
Content-Type: application/json
```

**Body**

```json
{
  "subject": "Your ticket subject",
  "body": "Your ticket body",
  "lang": "en"
}
```

**Response**

```json
{
  "urgency_score": 0.75,
  "urgency_reason": {
    "sentiment": "NEGATIVE",
    "confidence": 0.99,
    "rules_score": 0.7
  },
  "cluster_id": -1
}
```

#### Local launch

```bash
uvicorn src.api:app --reload --host 0.0.0.0 --port 8000
```

Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)

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

### 🐳 Docker / Docker‑Compose (optional)

1. **Build image**

   ```bash
   docker build -t ai-support-triage .
   ```

2. **Run**

   * API only

     ```bash
     docker run -p 8000:8000 --env API_KEY=$API_KEY ai-support-triage
     ```

   * Dashboard

     ```bash
     docker run -p 8501:8501 --env API_KEY=$API_KEY ai-support-triage streamlit run src/dashboard.py
     ```

3. **Compose**

   Create `.env`:

   ```env
   API_KEY=0123456789abcdef0123456789abcdef
   ```

   Launch both services:

   ```bash
   docker-compose up --build
   ```

   * API → [http://localhost:8000/docs](http://localhost:8000/docs)
   * Dashboard → [http://localhost:8501](http://localhost:8501)


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

*Includes unit & functional tests for PII masking, clustering, urgency scoring and full‑pipeline integration.*

---


## 👨‍💻 About the Author

**Jean-François Kantke**  
Senior Software Developer | 🇨🇦 Canadian & 🇫🇷 French  
NLP & Cloud Architecture Enthusiast  
📍 Montreal, QC, Canada  | 🔗 [LinkedIn](https://www.linkedin.com/in/jeanfrancoiskantke)

---

## 📄 License

MIT — see the [LICENSE](LICENSE) file for details.
