# K.A.O.S. ARM - Frontend CLI Client

**Component:** Distributed Kali-compatible CLI agent  
**Platform:** RHEL 8+, Ubuntu 20.04+  
**Container:** Podman (rootless) / Docker  
**Language:** Python 3.10+  

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run CLI
export BRAIN_HOST=127.0.0.1
export BRAIN_PORT=5000
python main.py
```

## Usage

```bash
# Interactive CLI
python main.py

# Enter commands at prompt
> scan network
> inject payload
> hello
```

## Core Modules

| Module | Purpose |
|--------|----------|
| `main.py` | CLI interface & session management |
| `validator.py` | Input validation |

## Features

- **Local Fallback:** Works offline with heuristic rules
- **Session Logging:** persistent to `/opt/arm/session.log`
- **ANSI Colors:** Terminal output formatting
- **Brain API:** Remote analysis via REST

## Deployment

```bash
ansible-playbook ops/ansible/deploy_arm.yml
```
*   **Backups:** Stored in `/opt/arm/backups`.

## 6. Troubleshooting

**Issue: "Permission denied" on network scans (Nmap)**  
*Resolution:* The container requires `NET_RAW` capabilities. Re-run the deployment playbook to recreate the container with the correct flags.

**Issue: "Insufficient UIDs or GIDs"**  
*Resolution:* Ensure `shadow-utils-subid` is installed and your user has entries in `/etc/subuid` and `/etc/subgid`. The playbook handles this automatically in Phase 2.5.

**Issue: Agent cannot connect to Brain**  
*Resolution:* Verify the `BRAIN_HOST` environment variable. By default, it attempts to connect to the Podman gateway (`172.17.0.1`).