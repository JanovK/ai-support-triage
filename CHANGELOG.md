# 📦 Changelog

## [1.0.0] – 2025-04-30
### Added
- Full end-to-end CLI pipeline: ingest → mask → cluster → score
- Streamlit dashboard with SHA256 authentication
- Dockerfile + dockerignore
- CI/CD GitHub Actions (test, cache, lint)
- Deployment on Streamlit Cloud with secrets
- Functional & unit tests (pytest)
- PII masking for names, phones, emails, addresses
- README and Streamlit config

### Changed
- README overhaul with deploy, Docker, CI, usage docs

### Security
- Hashed login with SHA256
