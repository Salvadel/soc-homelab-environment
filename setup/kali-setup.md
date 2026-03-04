# Kali Linux Setup

This document covers the installation and configuration of the Kali Linux virtual machine in the SOC homelab. Kali Linux serves as the designated attack machine, used to simulate threat actor behavior against the Windows 11 target endpoint. All activity from this machine is fully contained within the isolated LAN Segment.

## VM Specifications

| Property | Value |
|---|---|
| Operating System | Kali Linux |
| RAM | 4GB |
| CPUs | 2 |
| Storage | 50GB |
| Network Adapter | LAN Segment (Isolated) |
| IP Address | 192.168.100.30 |
| Role | Attack Machine |

## Installation

Kali Linux was installed as a virtual machine in VMware Workstation using the official Kali Linux ISO. During installation default settings were accepted with the exception of the network configuration which was set to the isolated LAN Segment after installation was complete.

### Kali Desktop

The screenshot below confirms the Kali Linux VM is fully installed and operational.

![Kali Desktop](../images/kali-desktop.png)

## Network Configuration

A static IP address was manually assigned to the Kali Linux VM to ensure consistent addressing within the isolated LAN Segment. No default gateway or DNS was configured as the LAN Segment has no routing to external networks.

### Static IP Assignment

| Property | Value |
|---|---|
| IP Address | 192.168.100.30 |
| Subnet Mask | 255.255.255.0 |
| Gateway | None |
| DNS | None |

The screenshot below shows the output of `ip a` confirming the static IP address has been correctly assigned to the Kali Linux VM.

![Kali IP Config](../images/kali-ip-config.png)

## System Update

After installation, the system package list and all installed packages were updated to ensure the latest libraries and security patches are in place before use in the lab.

```bash
sudo apt update && sudo apt upgrade -y
```

The screenshot below shows the terminal output confirming all packages are up to date.

## Connectivity Verification

After static IP assignment, connectivity to both other VMs on the LAN Segment was verified using ping to confirm the isolated network is functioning correctly.

### Kali → Windows 11

```bash
ping 192.168.100.20
```

![Windows 11 Ping Test](../images/ping-test-kali-to-windows)

### Kali → Ubuntu Server

```bash
ping 192.168.100.10
```
![Ubuntu Server Ping Test](../images/ping-test-kali-to-server)

## Role in Lab Exercises

Kali Linux is used exclusively as the simulated threat actor machine in this lab. Its role is to launch controlled attacks against the Windows 11 target endpoint, generating security events that are detected and alerted on by the Wazuh SIEM running on Ubuntu Server. This simulates the attacker side of a real SOC detection and response workflow.

Planned exercises using Kali include:

- **Network reconnaissance** — Using Nmap to scan the Windows 11 endpoint and enumerate open ports and services
- **Brute force attacks** — Using Hydra or Medusa to simulate credential stuffing and brute force login attempts against RDP and SMB on Windows 11
- **Exploitation** — Using Metasploit to simulate exploitation of vulnerabilities on the intentionally weakened Windows 11 endpoint
- **Post exploitation** — Simulating lateral movement and privilege escalation techniques after initial access is achieved

Each exercise is designed to generate meaningful alerts in the Wazuh dashboard that are then investigated and documented as individual projects in the `projects/` folder of this repository.

## Security Notes

- Kali Linux has no Wazuh agent installed, as it is the attack source rather than a monitored endpoint
- No intentional vulnerability configuration was applied to Kali — all offensive activity originates from this machine
- Kali has no internet access due to the isolated LAN Segment, meaning all tools used in exercises are pre-installed with the Kali distribution
- All attack activity is strictly contained within the isolated lab environment and does not affect any external systems or networks
