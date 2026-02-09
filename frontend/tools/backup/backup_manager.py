#!/usr/bin/env python3
"""
K.A.O.S. Backup Manager
Handles secure rotation and GPG signing of Arm client data.
"""

import os
import sys
import tarfile
import gnupg
import argparse
from datetime import datetime
import glob

# Configuration
BACKUP_DIR = "/opt/arm/backups"
SOURCE_DIR = "/opt/arm"
MAX_BACKUPS = 5
GPG_HOME = "/root/.gnupg"


def create_backup(dev_mode=False):
    """Create a timestamped tar.gz backup of the source directory.

    The archive is stored under BACKUP_DIR and will be signed.
    """
    if not os.path.exists(BACKUP_DIR):
        os.makedirs(BACKUP_DIR)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"kaos_arm_backup_{timestamp}.tar.gz"
    filepath = os.path.join(BACKUP_DIR, filename)

    print("Creating backup: " + filepath)

    # Create the tarball archive
    with tarfile.open(filepath, "w:gz") as tar:
        tar.add(SOURCE_DIR, arcname=os.path.basename(SOURCE_DIR))

    # Sign the backup artifact
    sign_backup(filepath, dev_mode)

    return filepath


def sign_backup(filepath, dev_mode):
    """Signs the backup file using GPG."""
    gpg = gnupg.GPG(gnupghome=GPG_HOME)

    # Check for existing private keys
    keys = gpg.list_keys()
    if not keys:
        if dev_mode:
            print("WARNING: No GPG keys found. Skipping signature (DEV MODE).")
            return
        else:
            print("CRITICAL: No GPG keys found! Cannot sign backup.")
            sys.exit(1)

    print("Signing " + filepath + "...")
    with open(filepath, "rb") as f:
        status = gpg.sign_file(f, detach=True, output=f"{filepath}.sig")

    if status.status != "sig created":
        print("ERROR: Failed to sign backup.")
        sys.exit(1)
    print("Signature created successfully.")


def rotate_backups():
    """Rotate backups, keeping only the last N files defined by
    MAX_BACKUPS.
    """
    print("Rotating backups...")
    # Find all tar.gz files
    files = glob.glob(os.path.join(BACKUP_DIR, "*.tar.gz"))
    files.sort(key=os.path.getmtime)

    if len(files) > MAX_BACKUPS:
        to_delete = files[:-MAX_BACKUPS]
        for f in to_delete:
            print(f"Removing old backup: {f}")
            os.remove(f)
            # Remove associated signature file if it exists
            if os.path.exists(f + ".sig"):
                os.remove(f + ".sig")
    else:
        print("No rotation needed.")


def main():
    parser = argparse.ArgumentParser(description="K.A.O.S. Backup Manager")
    parser.add_argument(
        "--dev", action="store_true", help="Skip GPG check for development"
    )
    args = parser.parse_args()

    try:
        create_backup(args.dev)
        rotate_backups()
        print("Backup process completed successfully.")
    except Exception as e:
        print(f"Backup failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
