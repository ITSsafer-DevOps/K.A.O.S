# K.A.O.S. (Ai-Kali-RHEL) - Ubuntu Deployment Edition


[![Project in development](https://img.shields.io/badge/status-development-orange)](https://github.com/ITSsafer-DevOps/K.A.O.S)

<p align="center">
    <a href="https://github.com/ITSsafer-DevOps/K.A.O.S" title="K.A.O.S. project">
        <img src="https://lh3.googleusercontent.com/a/ACg8ocL7Y3S3o2vpWe2l74S2i5i7vN3x_VpllvsaQCwwXIKEHyl8WB5WixuZtiPhofQaSMfix7XAb2T1cnYKCwr1b2S7J5bI6s3e=s288-c-no" alt="Project Logo" width="180" style="border-radius:12px;padding:6px;background:#fff;box-shadow:0 4px 14px rgba(0,0,0,0.12);border:1px solid rgba(0,0,0,0.06);"/>
    </a>
</p>

<p align="center" style="margin-top:10px;">
    <a href="https://www.redhat.com" title="Red Hat">
        <img src="https://vectorlogo.zone/logos/redhat/redhat-icon.svg" alt="Red Hat Hat" height="44" style="background:#fff;border-radius:6px;padding:4px;box-shadow:0 2px 8px rgba(0,0,0,0.08);" />
    </a>
    &nbsp;&nbsp;&nbsp;
    <a href="https://www.kali.org" title="Kali Linux">
        <img src="https://www.kali.org/images/kali-logo.svg" alt="Kali Linux" height="44" style="background:#fff;border-radius:6px;padding:4px;box-shadow:0 2px 8px rgba(0,0,0,0.08);" />
    </a>
    &nbsp;&nbsp;&nbsp;
    <a href="https://ubuntu.com" title="Ubuntu">
        <img src="https://assets.ubuntu.com/v1/29985a98-ubuntu-logo32.png" alt="Ubuntu" height="44" style="background:#fff;border-radius:6px;padding:4px;box-shadow:0 2px 8px rgba(0,0,0,0.08);" />
    </a>
</p>

**Note:** This project is under active development.

---

## Technologies Used

- Container runtime: Podman (rootless)
- OS: Red Hat Enterprise Linux (RHEL 8/9), Ubuntu (for dev/testing)
- Backend: Flask + Gunicorn + Gevent
- Serialization: orjson
- Retry/Resilience: Tenacity
- NLP/LLM: Ollama / Mistral / Llama
- CI/CD: GitHub Actions (lint + tests)
- Deployment: Ansible (atomic deploy, symlink rotation)
- Languages: Python 3.10+
- Security: SubUID/SubGID, CAP_NET_RAW (controlled), host-mounted audit volumes

---

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)  [![CI](https://github.com/ITSsafer-DevOps/K.A.O.S/actions/workflows/ci.yml/badge.svg)](.github/workflows/ci.yml)

Enterprise-grade Offensive AI Framework for RHEL-compatible environments.

Hybrid Offensive AI Framework for Enterprise Linux Environments.

## Technical Architecture

---

## Contact

Project lead: Kristián Kašník  
LinkedIn: [linkedin.com/in/kristián-kašník-03056a377](https://linkedin.com/in/kristián-kašník-03056a377)  
Email: [itssafer@itssafer.org](mailto:itssafer@itssafer.org)


```mermaid
graph TB
    subgraph "🏢 Enterprise Layer"
        A["🛡️ Ansible<br/>Orchestration"]
    end
    subgraph "🧠 AI/ML Layer"
        B["⚡ Gunicorn/Gevent<br/>Backend"]
        C["🔄 Hybrid Engine<br/>Fast-Path + LLM"]
    end
    subgraph "💾 Persistence & State"
        D["📁 Symlink<br/>Config Mgmt"]
        E["🔐 State<br/>Retention"]
    end
    subgraph "🔍 Intelligence Tiers"
        F["⚙️ Heuristic<br/>Fast-Path"]
        G["🧬 Deep Learning<br/>Analysis"]
    end
    A --> B
    B --> C
    C --> F
    C --> G
    B --> D
    D --> E
    style A fill:#c41c3b,stroke:#262626,color:#fff
    style B fill:#e74c3c,stroke:#262626,color:#fff
    style C fill:#e74c3c,stroke:#262626,color:#fff
    style D fill:#d35400,stroke:#262626,color:#fff
    style E fill:#d35400,stroke:#262626,color:#fff
    style F fill:#27ae60,stroke:#262626,color:#fff
    style G fill:#3498db,stroke:#262626,color:#fff
```

### High-Performance Backend (Gunicorn/Gevent)
Engineered for high-concurrency environments, the backend utilizes Gunicorn with Gevent workers to ensure non-blocking I/O operations, critical for real-time AI processing.

### Persistence Strategy (Symlinking)
Adopts a robust symlink-based architecture for configuration management and data persistence, ensuring seamless upgrades and state retention across container lifecycles.

### Enterprise Orchestration (Ansible Atomic Deploy)
Deployment logic is encapsulated in Ansible playbooks designed for atomicity. This guarantees that infrastructure changes are either fully applied or rolled back, preventing inconsistent states.

### Hybrid Intelligence (Fast-Path logic)
Features a tiered decision engine capable of executing rapid heuristic evaluations (Fast-Path) for immediate threats, while offloading complex analysis to deep learning models.
