# K.A.O.S. Brain - Cognitive Backend (Enterprise)

## Architecture

```ascii
   +-------------+        +-------------+        +-----------------+
   |   Frontend  | <----> |  Flask API  | <----> |  Hybrid Engine  |
   |    (Kali)   |  JSON  |  (Gunicorn) |        | (Regex + Risk)  |
   +-------------+        +-------------+        +--------+--------+
                                                          |
                                                          v
                                                 +-----------------+
                                                 |   Ollama LLM    |
                                                 | (Mistral/Llama) |
                                                 +-----------------+
```

## Overview
The K.A.O.S. Brain is the central cognitive processing unit for the security operations platform. It utilizes a hybrid approach combining deterministic regex heuristics for fast-path analysis and Large Language Models (LLM) for deep reasoning.

## Deployment

This repository utilizes an atomic Ansible deployment strategy with Systemd integration and automatic rollback capabilities.

### Prerequisites
- Ansible installed on control node.
- Target host accessible via SSH (or localhost).

### Run Deployment
Execute the following command from the project root:

```bash
ansible-playbook ops/ansible/deploy_brain.yml
```

## Features
- **Tenacity**: Robust retry logic for LLM connections.
- **Orjson**: High-performance JSON serialization.
- **Safety**: Pre-flight checks for destructive commands.
