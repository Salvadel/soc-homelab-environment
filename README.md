# SOC Homelab

A home Security Operations Center (SOC) lab built to simulate real-world threat detection and incident response workflows. The lab replicates a basic corporate network environment consisting of a monitored Windows endpoint, a SIEM server, and an attack machine — all isolated within a private virtual network. The purpose is to develop hands-on experience in attack simulation, log analysis, alert triage, and incident documentation, core skills required for SOC Analyst roles.

## Network Diagram

![Network Diagram](../images/network-diagram.png)

## Technologies Used

| Technology | Role |
|---|---|
| VMware Workstation | Hypervisor hosting all three virtual machines |
| Windows 11 Home | Target endpoint simulating a corporate workstation |
| Kali Linux | Attack machine used to simulate threat actor behavior |
| Ubuntu Server 24 | SIEM server hosting the full Wazuh stack |
| Wazuh | Open source SIEM for log collection, alerting, and dashboarding |
| Sysmon | Windows endpoint telemetry enhancement tool |

## Repository Structure
```
soc-homelab/
├── README.md
├── architecture/
│   ├── architecture-overview.md
│   ├── static-ip-config.md
│   └── images/
├── setup/
│   ├── vmware-setup.md
│   ├── windows11-setup.md
│   ├── kali-setup.md
│   ├── ubuntu-setup.md
│   ├── wazuh-setup.md
│   ├── wazuh-agent-setup.md
│   └── sysmon-setup.md
├── projects/
└── images/
```

## Table of Contents

### Architecture
Start here for a full understanding of the lab design, network topology, and the rationale behind every decision made.

| Document | Description |
|---|---|
| [Architecture Overview](architecture/architecture-overview.md) | Full lab design, machine roles, design decisions, known limitations, and future improvements |
| [Static IP Configuration](architecture/static-ip-config.md) | IP assignment table and connectivity verification between all three VMs |

### Setup
Follow these documents in order to rebuild the lab from scratch. Each document covers the installation and configuration of a single component.

| Order | Document | Description |
|---|---|---|
| 1 | [VMware Setup](setup/vmware-setup.md) | Hypervisor configuration, VM hardware specs, network isolation, and baseline snapshots |
| 2 | [Windows 11 Setup](setup/windows11-setup.md) | OS installation, network configuration, user accounts, and intentional vulnerability configuration |
| 3 | [Kali Linux Setup](setup/kali-setup.md) | OS installation, network configuration, system update, and lab exercise roles |
| 4 | [Ubuntu Server Setup](setup/ubuntu-setup.md) | OS installation, network configuration, and Wazuh service verification |
| 5 | [Wazuh Setup](setup/wazuh-setup.md) | Full Wazuh stack installation, dashboard access, and service verification |
| 6 | [Wazuh Agent Setup](setup/wazuh-agent-setup.md) | Agent installation on Windows 11, Sysmon log collection configuration, and troubleshooting |
| 7 | [Sysmon Setup](setup/sysmon-setup.md) | Sysmon installation, service configuration, and Wazuh integration |

### Projects
Documented attack simulation and detection exercises performed in the lab. Each project includes the attack methodology, Wazuh alerts generated, and investigation findings.

| Project | Description |
|---|---|
| Coming soon | — |
