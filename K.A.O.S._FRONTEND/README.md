# K.A.O.S. rm Client (Enterprise Edition)

**Product Version:** 1.0.0-RC1  
**Target Platform:** Red Hat Enterprise Linux (RHEL) 8/9  
**Container Engine:** Podman (Rootless)

## 1. Product Overview

The **K.A.O.S. Arm Client** is the secure frontend interface for the K.A.O.S. distributed intelligence system. It provides a containerized, ephemeral Kali Linux environment orchestrated by Podman on RHEL workstations. The client acts as a hybrid agent, bridging local execution capabilities with the "Brain" backend for command analysis and decision support.

## 2. Solution Architecture

The solution utilizes a rootless container architecture to ensure host security while providing necessary capabilities for security operations.

```text
+---------------------------------------------------------------+
|  RHEL WORKSTATION (Host)                                      |
|                                                               |
|  +---------------------------------------------------------+  |
|  |  Podman Rootless Namespace (User Scope)                 |  |
|  |                                                         |  |
|  |  +-----------------------+    HTTP/JSON    +---------+  |  |
|  |  |  [Container: kali-ai] | <-------------> |  BRAIN  |  |  |
|  |  |  -------------------  |                 | BACKEND |  |  |
|  |  |  • Python Agent       |                 +---------+  |  |
|  |  |  • Security Tools     |                              |  |
|  |  |  • ZSH Interface      |                              |  |
|  |  +----------+------------+                              |  |
|  |             |                                           |  |
|  +-------------|-------------------------------------------+  |
|                | Volume Mount (:Z)                            |
|      +---------v----------+                                   |
|      |  /opt/arm (Host)   |                                   |
|      +--------------------+                                   |
+---------------------------------------------------------------+
```

## 3. Prerequisites

*   **Operating System:** RHEL 8, RHEL 9, or Fedora.
*   **User Privileges:** Standard user with `sudo` access (required for initial package installation and namespace configuration).
*   **Network:** Outbound access to `docker.io` for image pulling.

## 4. Installation Procedure

The deployment is fully automated via Ansible. This process handles:
1.  Deep cleanup of legacy containers.
2.  Installation of Podman and `shadow-utils-subid`.
3.  Configuration of Rootless SubUID/SubGID namespaces.
4.  Provisioning of the Kali Linux container with `NET_RAW` capabilities.

### 4.1. Deploy
Run the playbook from the project root:

```bash
ansible-playbook ops/ansible/deploy_arm.yml --ask-become-pass
```

*Note: You will be prompted for your sudo password to configure system namespaces.*

## 5. Operational Guide

### 5.1. Accessing the Agent
A convenience script is installed to `~/bin/kali-ai`. Ensure this directory is in your `$PATH`.

```bash
# Launch the Hybrid Agent directly
~/bin/kali-ai
```

### 5.2. Manual Shell Access
To access the raw ZSH shell inside the container:

```bash
podman exec -it kali-ai /bin/zsh
```

### 5.3. Data Persistence
*   **Workspace:** All data in `src/kaos_arm` on the host is mounted to `/opt/arm` in the container.
*   **Backups:** Stored in `/opt/arm/backups`.

## 6. Troubleshooting

**Issue: "Permission denied" on network scans (Nmap)**  
*Resolution:* The container requires `NET_RAW` capabilities. Re-run the deployment playbook to recreate the container with the correct flags.

**Issue: "Insufficient UIDs or GIDs"**  
*Resolution:* Ensure `shadow-utils-subid` is installed and your user has entries in `/etc/subuid` and `/etc/subgid`. The playbook handles this automatically in Phase 2.5.

**Issue: Agent cannot connect to Brain**  
*Resolution:* Verify the `BRAIN_HOST` environment variable. By default, it attempts to connect to the Podman gateway (`172.17.0.1`).