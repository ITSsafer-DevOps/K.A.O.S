#!/usr/bin/env python3
"""
K.A.O.S. Enterprise Artifact Generator
Author: K.A.O.S. DevOps Team
Purpose: Master backup utility for generating release source archives.
"""

import sys
import tarfile
import hashlib
import logging
from datetime import datetime
from pathlib import Path

# Configure Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger("ArtifactGen")


def calculate_sha256(file_path: Path) -> str:
    """Calculates SHA256 hash of a file."""
    sha256_hash = hashlib.sha256()
    try:
        with open(file_path, "rb") as f:
            # Read in 4K chunks
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    except IOError as e:
        logger.error(f"Error reading file for checksum: {e}")
        sys.exit(1)


def get_exclusion_filter():
    """
    Returns a filter function for tarfile.add to exclude specific patterns.
    """

    def filter_func(tarinfo):
        name = tarinfo.name
        # tarinfo.name is the path inside the archive (e.g., ./folder/file)

        # Check for file extensions
        if name.endswith(".pyc") or name.endswith(".log"):
            return None

        # Check for directory/file names in the path
        path = Path(name)
        parts = path.parts

        # Exclusions list (Directories)
        exclusions = {".git", ".venv", "venv", "__pycache__", "backups"}

        # If any part of the path matches an exclusion, skip it
        for part in parts:
            if part in exclusions:
                return None

        return tarinfo

    return filter_func


def main():
    # 1. Directory Setup
    script_location = Path(__file__).resolve()
    if script_location.parent.name == "tools":
        project_root = script_location.parent.parent
    else:
        project_root = script_location.parent

    backup_dir = project_root / "backups"
    backup_dir.mkdir(exist_ok=True)

    # 2. Archive Creation
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    archive_filename = f"{project_root.name}_source_{timestamp}.tar.gz"
    archive_path = backup_dir / archive_filename

    logger.info(f"📦 Starting archive creation for: {project_root}")
    logger.info(f"📍 Destination: {archive_path}")

    try:
        with tarfile.open(archive_path, "w:gz") as tar:
            tar.add(project_root, arcname=".", filter=get_exclusion_filter())

        size_mb = archive_path.stat().st_size / (1024 * 1024)
        logger.info(f"✅ Archive created successfully ({size_mb:.2f} MB)")

        # 3. Integrity Verification
        logger.info("🔐 Generating SHA256 checksum...")
        file_hash = calculate_sha256(archive_path)

        hash_filename = f"{archive_filename}.sha256"
        hash_path = backup_dir / hash_filename

        with open(hash_path, "w") as f:
            f.write(f"{file_hash}  {archive_filename}\n")

        logger.info(f"✅ Checksum saved to: {hash_filename}")
        logger.info(f"#️⃣  SHA256: {file_hash}")

    except Exception as e:
        logger.error(f"❌ Operation failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
