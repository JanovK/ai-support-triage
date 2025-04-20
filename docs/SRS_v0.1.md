# Software Requirements Specification (SRS)
**Project Name:** AI Support Triage  
**Author:** Jean-François Kantke  
**Program:** MSIT Capstone – University of the People  
**Version:** 0.1  
**Date:** April 2025

---

## 1. Introduction

### 1.1 Purpose
This document defines the requirements for the AI Support Triage platform. The system uses NLP and ML to automate ticket ingestion, PII masking, clustering, urgency scoring, and queue prioritization.

### 1.2 Scope
This MVP is intended for small to mid-sized support teams facing growing ticket loads. The tool will help optimize agent workflow, reduce MTTR, and comply with privacy regulations (GDPR, HIPAA-lite).

### 1.3 References
- CRISP-DM model
- IEEE 830 SRS guidelines
- Hugging Face Transformers docs
- SpaCy pipelines
- GDPR, HIPAA security frameworks

---

## 2. Overall Description

### 2.1 Product Functions
- Ingest multichannel tickets (JSON, email)
- Mask sensitive data (PII, PHI)
- Detect language and cluster tickets by topic
- Score urgency of incoming requests
- Prioritize queue based on severity and business rules
- Provide explainable scoring and real-time dashboards

### 2.2 User Personas
| Role | Need |
|------|------|
| Support Agent | Work with pre-sorted, urgent tickets |
| Admin | Monitor system performance and compliance |
| Developer | Maintain, test, extend the system |

---

## 3. Functional Requirements

| ID  | Description | Priority | Acceptance Test |
|-----|-------------|----------|------------------|
| FR1 | Ingest tickets from file or API | High | Unit test ingestion |
| FR2 | Detect and mask PII | High | Regex & NER test |
| FR3 | Detect ticket language | Medium | langdetect test |
| FR4 | Cluster tickets semantically | High | HDBSCAN cluster validation |
| FR5 | Score urgency of ticket | High | Score threshold test |
| FR6 | Sort queue based on priority | Medium | Queue sorting test |
| FR7 | Display dashboard to user | Low | Manual test in browser |

---

## 4. Non-Functional Requirements

| ID | Requirement | Target |
|----|-------------|--------|
| NFR1 | Max latency per ticket | < 2s |
| NFR2 | Data encryption | TLS 1.3, AES-256 |
| NFR3 | Local/Cloud deployability | Docker + CLI |
| NFR4 | Traceability / audit | SHAP or LIME explanations |
| NFR5 | Security compliance | GDPR / HIPAA-lite ready |

---

## 5. Traceability Matrix

| User Story | Requirement(s) |
|------------|----------------|
| As an agent, I want critical tickets first | FR4, FR5, FR6 |
| As a company, I want to protect client data | FR2, NFR2, NFR5 |
| As a developer, I want reproducible builds | NFR3 |

---

## 6. Glossary

- **PII**: Personally Identifiable Information  
- **NER**: Named Entity Recognition  
- **MTTR**: Mean Time to Resolve  
- **HDBSCAN**: Hierarchical DBSCAN (clustering algorithm)  
- **SHAP/LIME**: Explainability tools for ML models
