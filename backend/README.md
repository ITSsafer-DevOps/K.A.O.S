# K.A.O.S. Brain - Backend Analysis Engine

**Component:** LLM-powered REST API with heuristic analyzer  
**Framework:** Flask + Gunicorn  
**Language:** Python 3.10+  
**Port:** 5000 (development), configurable via env  

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run server
export OLLAMA_URL=http://localhost:11434/api/generate
export OLLAMA_MODEL=mistral
python -m flask run --host=0.0.0.0 --port=5000
```

## Endpoints

- `GET /api/v1/health` - Health check
- `POST /api/v1/analyze` - Command analysis (heuristic + LLM)

## Core Modules

| Module | Purpose |
|--------|----------|
| `app/main.py` | Flask application & routing |
| `core/analyzer.py` | Risk assessment & pattern matching |
| `core/validator.py` | Input validation |

## Configuration

Environment variables (see `config/settings.py`):
- `OLLAMA_URL` - LLM endpoint
- `OLLAMA_MODEL` - Model name (default: mistral)
- `OLLAMA_TIMEOUT` - Timeout in seconds (default: 10)
- `OLLAMA_RETRIES` - Retry attempts (default: 3)

## Deployment

```bash
ansible-playbook ops/ansible/deploy_brain.yml
```
