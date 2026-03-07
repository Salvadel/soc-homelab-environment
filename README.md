# SOC Homelab

A home Security Operations Center (SOC) lab built to simulate real-world threat detection and incident response workflows. The lab replicates a basic corporate network environment consisting of a monitored Windows endpoint, a SIEM server, a SOAR automation server, a firewall, and an attack machine - all connected through a pfSense managed internal network. The purpose is to develop hands-on experience in attack simulation, log analysis, alert triage, automated response workflows, and incident documentation - core skills required for SOC Analyst roles.

## Network Diagram

![SOC Network Diagram](images/network-diagram.png)

## Technologies Used

| Technology | Role |
|---|---|
| VMware Workstation | Hypervisor hosting all five virtual machines |
| pfSense | Network perimeter firewall and router |
| Windows 11 Home | Target endpoint simulating a corporate workstation |
| Kali Linux | Attack machine used to simulate threat actor behavior |
| Ubuntu Server 24 - SIEM | SIEM server hosting the full Wazuh stack |
| Ubuntu Server 24 - SOAR | SOAR server hosting Shuffle and TheHive |
| Wazuh | Open source SIEM for log collection, alerting, and dashboarding |
| Sysmon | Windows endpoint telemetry enhancement tool |
| Shuffle | Open source SOAR platform for automated alert response workflows |
| TheHive | Open source case management platform for incident investigation |
| Slack | Analyst notification platform integrated with Shuffle |

## Repository Structure
```
soc-homelab/
├── README.md
├── architecture/
│   ├── architecture-overview.md
│   ├── static-ip-configuration.md
│   └── images/
│       ├── network-diagram.png
│       └── data-flow-diagram.png
├── setup/
│   ├── vmware-setup.md
│   ├── pfsense-setup.md
│   ├── windows11-setup.md
│   ├── kali-setup.md
│   ├── siem-server-setup.md
│   ├── wazuh-setup.md
│   ├── wazuh-agent-setup.md
│   ├── sysmon-setup.md
│   ├── soar-server-setup.md
│   ├── shuffle-setup.md
│   └── thehive-setup.md
├── projects/
│   └── 01-siem-soar-automation/
│       ├── README.md
│       ├── overview.md
│       ├── shuffle-workflow.md
│       ├── thehive-integration.md
│       ├── testing-and-results.md
│       └── images/
└── images/
```

## Table of Contents

### Architecture
Start here for a full understanding of the lab design, network topology, data flow, and the rationale behind every decision made.

| Document | Description |
|---|---|
| [Architecture Overview](architecture/architecture-overview.md) | Full lab design, machine roles, data flow diagram, design decisions, known limitations, and future improvements |
| [Static IP Configuration](architecture/static-ip-configuration.md) | IP assignment table and connectivity verification between all five VMs |

### Setup
Follow these documents in order to rebuild the lab from scratch. Each document covers the installation and configuration of a single component.

| Order | Document | Description |
|---|---|---|
| 1 | [VMware Setup](setup/vmware-setup.md) | Hypervisor configuration, VM hardware specs, network configuration, and baseline snapshots |
| 2 | [pfSense Setup](setup/pfsense-setup.md) | Firewall installation, WAN and LAN adapter configuration, and traffic routing verification |
| 3 | [Windows 11 Setup](setup/windows11-setup.md) | OS installation, network configuration, user accounts, and intentional vulnerability configuration |
| 4 | [Kali Linux Setup](setup/kali-setup.md) | OS installation, network configuration, system update, and lab exercise roles |
| 5 | [Ubuntu Server - SIEM Setup](setup/siem-server-setup.md) | OS installation, network configuration, and Wazuh service verification |
| 6 | [Wazuh Setup](setup/wazuh-setup.md) | Full Wazuh stack installation, dashboard access, and service verification |
| 7 | [Wazuh Agent Setup](setup/wazuh-agent-setup.md) | Agent installation on Windows 11, Sysmon log collection configuration, and troubleshooting |
| 8 | [Sysmon Setup](setup/sysmon-setup.md) | Sysmon installation, service configuration, and Wazuh integration |
| 9 | [Ubuntu Server - SOAR Setup](setup/soar-server-setup.md) | OS installation, network configuration, and Docker installation |
| 10 | [Shuffle Setup](setup/shuffle-setup.md) | Shuffle installation, Wazuh webhook configuration, and automation workflow setup |
| 11 | [TheHive Setup](setup/thehive-setup.md) | TheHive installation, Shuffle integration, and case management configuration |

### Projects
Documented attack simulation and detection exercises performed in the lab. Each project includes the attack methodology, Wazuh alerts generated, investigation findings, and incident response documentation.

| Project | Description |
|---|---|
| Coming soon | - |
