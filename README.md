# 🧠 AI Support Triage

Welcome to the official repository of **AI Support Triage** — a solo Capstone Project developed as part of the *Master of Science in Information Technology* at University of the People.

This platform leverages modern **Natural Language Processing (NLP)** and **MLOps** practices to **analyze**, **prioritize**, and **secure** multichannel support tickets (email, chat, JSON streams), enabling service teams to respond faster, reduce SLA violations, and limit data exposure risks.

---

## 🚀 Project Objective

Modern support operations face three key challenges:
- Overwhelming ticket **volume** (email, chat, voice-to-text)
- Growing **velocity** of multichannel customer queries
- **Vulnerability** due to unmasked PII and inconsistent triage

**AI Support Triage** provides an intelligent mechanism to:
- Mask sensitive data (GDPR, HIPAA-aware)
- Detect language, cluster ticket topics, and score urgency
- Prioritize cases using explainable AI and ML-based sorting

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
| Dashboards           | `Streamlit`, `ClickHouse`                 | Insights on volume, topics, and urgency |

---

## 📂 Project Structure

```bash
ai-support-triage/
├── docs/                    # SRS, references, diagrams
│   └── SRS_v0.1.md
├── src/                     # Core backend logic
│   ├── ingest.py
│   ├── mask_pii.py
│   ├── cluster_topics.py
│   ├── score_urgency.py
│   └── prioritize.py
├── tests/                   # Unit tests (pytest)
├── notebooks/               # Exploratory analysis
├── .github/workflows/       # GitHub Actions CI
├── .env.example             # Env vars template
├── requirements.txt
├── README.md
└── LICENSE
```

---

## 🧪 Running Locally

```bash
# Clone the repo
git clone https://github.com/JanovK/ai-support-triage.git
cd ai-support-triage

# Set up environment
./setup.sh # On Linux / macOS
setup.bat # On Windows
source venv/bin/activate

# Run local test
pytest tests/

# Start ingestion module
python src/ingest.py --config configs/demo.yaml

```

---

## 📅 Roadmap (Capstone Phases)

- ✅ Week 1: Requirement Analysis (SRS, skills audit, legal constraints)
- ✅ Week 2: Data ingestion & PII masking module
- 🔄 Week 3: Clustering + Urgency scoring + Dashboard MVP
- 🔜 Week 4: A/B testing, explainability, final polish

---

## 👨‍💻 About the Author

**Jean-François Kantke**  
Senior Software Developer | 🇨🇦 Canadian & 🇫🇷 French  
NLP & Cloud Architecture Enthusiast  
📍 Montreal, QC, Canada  | 🔗 [LinkedIn](https://www.linkedin.com/in/jeanfrancoiskantke)

---

## 📄 License

This project is licensed under the MIT License — see the LICENSE file for details.