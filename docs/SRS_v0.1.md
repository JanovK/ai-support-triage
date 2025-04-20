# Software Requirements Specification (SRS)
## 1. Introduction
- Project name: AI-Driven Ticket Intelligence Platform
- Purpose of the document
- Target audience: Developers, stakeholders, academic evaluators

## 2. Overall Description
- Problem summary
- Business goals
- User personas (support agent, admin, end-user)
- Constraints (budget $0, compute limits, regulatory)

## 3. Functional Requirements
| ID | Requirement | Priority | Test Method |
|----|-------------|----------|-------------|
| FR1 | System ingests tickets from email/JSON | High | Unit test ingest function |
| FR2 | Detect and mask PII in tickets | High | Regex test suite |
| FR3 | Detect ticket language | Medium | Cross-validation on langdetect |
| FR4 | Group tickets by topic | High | HDBSCAN evaluation |
| FR5 | Score urgency | High | A/B threshold test |
| FR6 | Prioritize queue | Medium | Simulated sorting test |
| FR7 | Display in dashboard | Low | Manual UI review |

## 4. Non-Functional Requirements
| ID | Requirement | Target |
|----|-------------|--------|
| NFR1 | Latency per ticket | < 2s |
| NFR2 | Data encryption | TLS 1.3, AES-256 |
| NFR3 | Deployment | CLI + Docker-ready |
| NFR4 | Logging / traceability | Full audit trail |
| NFR5 | Compliance support | GDPR, HIPAA-lite |
| NFR6 | Availability | > 95% uptime (if hosted) |

## 5. Traceability Matrix
| User Story | Requirements |
|------------|--------------|
| As an agent, I want sensitive data masked | FR2, NFR2, NFR5 |
| As a system, I want to flag urgent tickets | FR5 |
| As a project owner, I want the code to run locally | NFR3 |

## 6. Glossary
PII, MTTR, SLA, BERT, HDBSCAN, PPO, CI/CD
