#!/usr/bin/env python3
"""
K.A.O.S. Enterprise Release Finalizer
Author: K.A.O.S. DevOps Team
Purpose: Automates final preparation steps for Enterprise Release 1.0 (Ubuntu Target).
"""

import subprocess
import sys
import logging
from pathlib import Path

# Configure Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S"
)
logger = logging.getLogger("ReleaseMgr")

def run_cmd(command: str, cwd: Path, ignore_errors: bool = False) -> subprocess.CompletedProcess:
    """Executes a shell command with error handling."""
    try:
        result = subprocess.run(
            command,
            cwd=cwd,
            shell=True,
            check=not ignore_errors,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        return result
    except subprocess.CalledProcessError as e:
        if not ignore_errors:
            logger.error(f"❌ Command failed: {command}")
            logger.error(f"Error output: {e.stderr.strip()}")
            sys.exit(1)
        return e

def phase_1_git_ops(root_dir: Path):
    """Initializes Git, configures ignores, and commits state."""
    logger.info("🔧 PHASE 1: GIT REPOSITORY MANAGEMENT")
    
    git_dir = root_dir / ".git"
    if not git_dir.exists():
        logger.info("  • Initializing Git repository...")
        run_cmd("git init", root_dir)
    else:
        logger.info("  • Git repository already active.")

    gitignore = root_dir / ".gitignore"
    ignores = [
        "__pycache__/", "*.pyc", ".venv/", "venv/", 
        ".env", "backups/", "*.log", ".DS_Store"
    ]
    
    logger.info("  • Configuring .gitignore...")
    with open(gitignore, "w") as f:
        f.write("\n".join(ignores) + "\n")

    logger.info("  • Snapshotting codebase...")
    run_cmd("git add .", root_dir)
    
    # Commit with specific message, ignore error if clean
    res = run_cmd('git commit -m "Enterprise Release 1.0 - Ubuntu Deployment Ready"', root_dir, ignore_errors=True)
    if res.returncode == 0:
        logger.info("  ✅ Codebase committed.")
    elif "nothing to commit" in res.stdout:
        logger.info("  ✅ Working tree clean, nothing to commit.")
    else:
        logger.warning(f"  ⚠️ Commit status unknown: {res.stderr.strip()}")

def phase_2_docs(root_dir: Path):
    """Updates README.md with technical specifications."""
    logger.info("📄 PHASE 2: PROFESSIONAL DOCUMENTATION")
    
    readme_path = root_dir / "README.md"
    content = """# K.A.O.S. (Ai-Kali-RHEL) - Ubuntu Deployment Edition

Hybrid Offensive AI Framework for Enterprise Linux Environments.

## Technical Architecture

### High-Performance Backend (Gunicorn/Gevent)
Engineered for high-concurrency environments, the backend utilizes Gunicorn with Gevent workers to ensure non-blocking I/O operations, critical for real-time AI processing.

### Persistence Strategy (Symlinking)
Adopts a robust symlink-based architecture for configuration management and data persistence, ensuring seamless upgrades and state retention across container lifecycles.

### Enterprise Orchestration (Ansible Atomic Deploy)
Deployment logic is encapsulated in Ansible playbooks designed for atomicity. This guarantees that infrastructure changes are either fully applied or rolled back, preventing inconsistent states.

### Hybrid Intelligence (Fast-Path logic)
Features a tiered decision engine capable of executing rapid heuristic evaluations (Fast-Path) for immediate threats, while offloading complex analysis to deep learning models.
"""
    try:
        with open(readme_path, "w") as f:
            f.write(content)
        logger.info(f"  ✅ README.md updated: {readme_path}")
    except IOError as e:
        logger.error(f"❌ Failed to write README: {e}")
        sys.exit(1)

def phase_3_syntax(root_dir: Path):
    """Validates Ansible playbooks."""
    logger.info("🔍 PHASE 3: PRE-FLIGHT SYNTAX CHECK")
    
    playbooks = [
        "K.A.O.S._BACKEND/ops/ansible/deploy_brain.yml",
        "K.A.O.S._FRONTEND/ops/ansible/deploy_arm.yml"
    ]
    
    for pb_rel in playbooks:
        pb_path = root_dir / pb_rel
        if not pb_path.exists():
            logger.error(f"❌ Playbook missing: {pb_path}")
            sys.exit(1)
            
        logger.info(f"  • Checking: {pb_path.name}")
        res = run_cmd(f"ansible-playbook --syntax-check {pb_path}", root_dir, ignore_errors=True)
        if res.returncode == 0:
            logger.info(f"  ✅ Syntax Valid: {pb_path.name}")
        else:
            logger.error(f"❌ Syntax Error in {pb_path.name}")
            print(res.stderr)
            sys.exit(1)

def phase_4_artifacts(root_dir: Path):
    """Generates release artifacts."""
    logger.info("📦 PHASE 4: ARTIFACT SHIPMENT PREP")
    
    generator = root_dir / "tools/artifact_generator.py"
    if not generator.exists():
        logger.error(f"❌ Generator tool missing: {generator}")
        sys.exit(1)
        
    logger.info("  • Invoking artifact generator...")
    # Using sys.executable to ensure we use the same python interpreter
    res = run_cmd(f"{sys.executable} {generator}", root_dir)
    
    if res.returncode == 0:
        logger.info("  ✅ Artifacts generated successfully.")
    else:
        logger.error("❌ Artifact generation failed.")
        sys.exit(1)

def main():
    # Determine project root (assuming script is in root)
    root_dir = Path(__file__).resolve().parent
    
    print("\n" + "="*60)
    print("   K.A.O.S. RELEASE FINALIZER - UBUNTU EDITION")
    print("="*60 + "\n")
    
    phase_1_git_ops(root_dir)
    print("")
    phase_2_docs(root_dir)
    print("")
    phase_3_syntax(root_dir)
    print("")
    phase_4_artifacts(root_dir)
    
    print("\n" + "="*60)
    print("   ✅ RELEASE READY FOR DEPLOYMENT")
    print("="*60 + "\n")

if __name__ == "__main__":
    main()