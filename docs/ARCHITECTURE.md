# K.A.O.S. Enterprise Architecture Document

**Version:** 1.0  
**Date:** 2026-02-09  
**Classification:** Technical Design Document  

---

## 1. Executive Summary

K.A.O.S. (Kinetic Automated Operational System) je distribuovaný hybrid viacvrstvový AI/ML bezpečnostný systém skomponovaný z dvoch hlavných komponentov:

- **Frontend (ARM)**: Distribuovaný Kali Linux CLI klient s lokálnym fallback
- **Backend (Brain)**: LLM-powered analytický engine s heuristických pravidiel

**Architecture Pattern:** Microservices (Frontend-Backend separation)  
**Total Lines of Code:** 839  
**Security Posture:** Enterprise-Grade (0 critical issues)

---

## 2. System Architecture

### 2.1 Layered Architecture

```
┌──────────────────────────────────────────────────┐
│          CLI Interface (Frontend ARM)             │
│  - Command Input Processing                      │
│  - Session Management                            │
│  - Local Fallback Rules                          │
│  - ANSI Output Formatting                        │
└──────────────────────────────────────────────────┘
                        │
                   HTTP/REST API
                        │
┌──────────────────────────────────────────────────┐
│      API Gateway & Validation Layer               │
│  - Request/Response Serialization (orJSON)       │
│  - Retry Logic (Tenacity)                        │
│  - Health Checks                                 │
└──────────────────────────────────────────────────┘
                        │
┌──────────────────────────────────────────────────┐
│    Analysis Engine (Backend Brain)                │
│  ┌────────────────────────────────────────────┐  │
│  │  Heuristic Analyzer                        │  │
│  │  - Regex Pattern Matching                  │  │
│  │  - Risk Assessment (SAFE/MEDIUM/HIGH/CRIT)│  │
│  │  - Tool Type Classification                │  │
│  │  - Destructive Command Detection           │  │
│  └────────────────────────────────────────────┘  │
│  ┌────────────────────────────────────────────┐  │
│  │  LLM Query Layer (Ollama)                  │  │
│  │  - Model: Mistral (configurable)           │  │
│  │  - Retry Strategy (3 attempts, 2s delay)   │  │
│  │  - Streaming Disabled (batch processing)   │  │
│  └────────────────────────────────────────────┘  │
│  ┌────────────────────────────────────────────┐  │
│  │  Validator                                 │  │
│  │  - Input Sanitization                      │  │
│  │  - Output Verification                     │  │
│  └────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────┘
                        │
┌──────────────────────────────────────────────────┐
│        Persistent Store & Logging                │
│  - Session Logs (/opt/arm/session.log)          │
│  - Application Logs (Flask logging)              │
│  - Backup & Artifact Management                  │
└──────────────────────────────────────────────────┘
```

### 2.2 Component Breakdown

#### Frontend (ARM Module)
- **Location:** `frontend/src/kaos_arm/`
- **Files:** 3 (main.py, validator.py, requirements.txt)
- **Lines of Code:** 216
- **Dependencies:** colorama, requests, subprocess

**Responsibilities:**
1. CLI command input processing
2. Session persistence management
3. Remote Brain API communication
4. Local fallback heuristics
5. ANSI terminal formatting

#### Backend (Brain Module)
- **Location:** `backend/src/brain/`
- **Files:** 5 (main.py, analyzer.py, validator.py, core/*, requirements.txt)
- **Lines of Code:** 202
- **Dependencies:** Flask, requests, tenacity, orjson, Ollama API

**Responsibilities:**
1. Flask REST API endpoint serving
2. Command analysis with heuristics
3. LLM query forwarding
4. Response formatting
5. Health monitoring

#### Support Modules
- **Scripts:** `scripts/` (releases, artifacts) - 328 LOC
- **Tools:** `frontend/tools/backup/` (GPG signing, backups) - 108 LOC
- **Ops:** Ansible playbooks for deployment

---

## 3. Design Patterns

### 3.1 Retry Pattern (Tenacity)
```python
@retry(
    stop=stop_after_attempt(3),
    wait=wait_fixed(2),
    retry=retry_if_exception_type(requests.exceptions.ConnectionError),
)
```
**Usage:** LLM queries to Ollama API  
**Rationale:** Network resilience for external ML service

### 3.2 Fallback Pattern
```python
# Frontend -> Brain API (primary)
# On failure -> Local heuristics (fallback)
```
**Usage:** When Brain service is unavailable  
**Rationale:** Graceful degradation of functionality

### 3.3 Layered Validation
```
Input Validation → Heuristic Analysis → LLM Processing → Output Validation
```
**Usage:** All command processing pipelines  
**Rationale:** Defense-in-depth security model

### 3.4 Enumeration Pattern
```python
class RiskLevel(Enum):
    SAFE, MEDIUM, HIGH, CRITICAL
class ToolType(Enum):
    NMAP, SQLMAP, METASPLOIT, CONVERSATION, ...
```
**Usage:** Type-safe classification  
**Rationale:** Prevent string-based bugs, improve IDE support

---

## 4. Communication Protocol

### 4.1 Frontend → Backend (HTTP REST)

**Endpoint:** `POST /api/v1/analyze`

**Request Schema:**
```json
{
  "command": "string",
  "session_id": "string"
}
```

**Response Schema:**
```json
{
  "llm_layer": {
    "command": "string",
    "reasoning": "string"
  },
  "heuristic_layer": {
    "risk_level": "SAFE|MEDIUM|HIGH|CRITICAL",
    "tool_type": "string",
    "flags": ["string"]
  }
}
```

### 4.2 Backend → LLM (Ollama HTTP API)

**Endpoint:** `POST /api/generate` (configurable)  
**Model:** Mistral (default, configurable via `OLLAMA_MODEL`)  
**Timeout:** 10 seconds  
**Retry:** 3 attempts, 2-second delay

---

## 5. Data Models & Flow

### 5.1 Command Lifecycle

```
[1. CLI Input] → [2. Persistence] → [3. Brain API Call] → [4. Heuristic Analysis]
                                           ↓
                                    [5. LLM Query]
                                           ↓
                                    [6. Response Format]
                                           ↓
                                    [7. Output Display]
```

### 5.2 Risk Assessment Engine

**Destructive Patterns Detected:**
- `rm -rf` (recursive deletion)
- `mkfs` (filesystem formatting)
- Fork bombs (`:(){:|:&};:`)
- `dd` from `/dev/zero` (disk overwriting)
- `chmod 777 /` (permission escalation)

**Intent Mapping:**
| Keyword | Tool Type | Risk |
|---------|-----------|------|
| scan, map | NMAP | MEDIUM |
| inject | SQLMAP | HIGH |
| hello, hi | CONVERSATION | SAFE |
| (destructive) | ANY | CRITICAL |

---

## 6. Configuration Management

### 6.1 Environment Variables

**Backend (Brain):**
```bash
OLLAMA_URL=http://localhost:11434/api/generate
OLLAMA_MODEL=mistral
KAOS_HOST=127.0.0.1
KAOS_PORT=5000
```

**Frontend (ARM):**
```bash
BRAIN_HOST=127.0.0.1
BRAIN_PORT=5000
SESSION_LOG=/opt/arm/session.log
```

### 6.2 Configuration Layers
1. **Environment variables** (runtime, highest priority)
2. **Defaults** (code-level, lowest priority)
3. **Ansible playbooks** (infrastructure-level)

---

## 7. Security Architecture

### 7.1 Defense-in-Depth

| Layer | Mechanism | Status |
|-------|-----------|--------|
| Input | Regex validation, pattern matching | ✅ Active |
| Process | Subprocess text mode, error handling | ✅ Active |
| Network | HTTPS-capable, GPG signing | ✅ Configured |
| Output | Response validation, escaping | ✅ Active |

### 7.2 Threat Model

**Threats Mitigated:**
- Command injection (heuristic analysis + validation)
- DoS attacks (timeout, retry limits)
- Unsafe subprocess execution (text parameter usage)
- Credential exposure (no hardcoded secrets)

**Residual Risks:**
- LLM hallucinations (mitigated by heuristics)
- Network interception (use HTTPS in production)

---

## 8. Deployment Model

### 8.1 Container Architecture

**Backend (Brain):**
- Base: Python 3.9+
- Entry: `python -m flask run`
- Port: 5000
- Dependencies: Flask, orJSON, Tenacity, Requests

**Frontend (ARM):**
- Base: Kali Linux (or compatible)
- Entry: `python kaos_arm/main.py`
- Interactive: CLI with colorama output
- Dependencies: colorama, requests

### 8.2 Infrastructure (Ansible)

- `backend/ops/ansible/deploy_brain.yml`: Backend provisioning
- `frontend/ops/ansible/deploy_arm.yml`: Frontend deployment

---

## 9. Performance Characteristics

### 9.1 Metrics

| Metric | Value | Notes |
|--------|-------|-------|
| Frontend Response Time | <100ms | Local fallback |
| Backend Latency | 2-10s | LLM query overhead |
| LLM Timeout | 10s | Configurable |
| Max Retries | 3 | Exponential backoff-ready |
| Code Size | 839 LOC | Lean microservices |

### 9.2 Scalability

- **Horizontal:** Stateless design allows multiple Brain instances (load balanced)
- **Vertical:** LLM queries benefit from GPU acceleration
- **Caching:** Response caching not yet implemented (future optimization)

---

## 10. Future Enhancements

### Phase 2 (Planned)
1. **Caching Layer:** Redis for LLM response caching
2. **Database:** Persistent command history (PostgreSQL)
3. **Authentication:** API key/JWT validation
4. **Monitoring:** Prometheus metrics & Grafana dashboards
5. **Testing:** Unit tests, integration tests, E2E tests
6. **Documentation:** Swagger/OpenAPI specification

### Phase 3 (Vision)
1. **Multi-tenancy:** Isolated user sessions
2. **Analytics:** Command usage patterns
3. **ML fine-tuning:** Custom model training
4. **Federation:** Distributed Brain clusters

---

## 11. Compliance & Standards

- **Code Standard:** PEP 8 (Python)
- **Security:** OWASP Top 10 mitigations
- **Logging:** Structured logging (Flask + Python logging)
- **License:** [See LICENSE file]

---

## 12. Glossary

| Term | Definition |
|------|-----------|
| ARM | Agent Response Module (Frontend) |
| Brain | Backend analytical engine |
| LLM | Large Language Model (Ollama) |
| Heuristic | Rule-based pattern matching |
| Fallback | Local logic when Brain is unavailable |
| Tenacity | Python retry library |
| orJSON | Fast JSON serialization |

---

**Document Owner:** K.A.O.S. Development Team  
**Last Updated:** 2026-02-09  
**Status:** Active
