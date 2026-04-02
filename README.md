# SOC Homelab

A home Security Operations Center (SOC) lab designed for simulating real-world threat detection and response scenarios. The lab is designed to mimic a basic corporate network infrastructure with a monitored Windows endpoint, SIEM server, SOAR server, firewall, and attack machine, all connected through a pfSense-managed internal network. The goal is to gain practical knowledge and experience in attack simulation, log analysis, and response, which are critical for becoming a SOC Analyst.

## Network Diagram

![SOC Network Diagram](images/network-diagram.png)

## Technologies Used

| Technology | Role |
|---|---|
| VMware Workstation | Hypervisor hosting all five virtual machines |
| pfSense | Network perimeter firewall and router |
| Windows 11 Home | Target endpoint simulating a corporate workstation |
| Kali Linux | Attack machine used to simulate threat actor behavior |
| Ubuntu Server - SIEM | SIEM server hosting the full Wazuh stack |
| Ubuntu Server - SOAR | SOAR server hosting Shuffle, TheHive, and IOC enrichment integrations |
| Wazuh | Open source SIEM for log collection, alerting, and dashboarding |
| Sysmon | Windows endpoint telemetry enhancement tool |
| Shuffle | Open source SOAR platform for automated alert response workflows |
| TheHive | Open source case management platform for incident investigation |
| Slack | Analyst notification platform integrated with Shuffle |
| VirusTotal | IOC enrichment - IP, hash, and URL reputation lookups |
| AbuseIPDB | IOC enrichment - IP reputation and abuse reporting |

## Repository Structure
```
soc-homelab/
├── README.md
├── architecture/
│   ├── architecture-overview.md
│   ├── static-ip-configuration.md
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
└── images/
```

## Table of Contents

### Architecture
Start here for a full understanding of the lab design, network topology, data flow, and the rationale behind design decisions. 

| Document | Description |
|---|---|
| [Architecture Overview](architecture/architecture-overview.md) | Full lab design, machine roles, data flow diagram, design decisions, known limitations, and future improvements |
| [Static IP Configuration](architecture/static-ip-configuration.md) | IP assignment table and connectivity verification between all five VMs |

### Setup
Follow these documents to build the lab environment. Each document covers the installation and configuration of a single component.

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
| 10 | [Shuffle Setup](setup/shuffle-setup.md) | Shuffle installation, Wazuh webhook configuration, IOC enrichment integration, and automation workflow setup |
| 11 | [TheHive Setup](setup/thehive-setup.md) | TheHive installation, Shuffle integration, and case management configuration |

### Projects
Documented projects performed by the SOC-lab, full documentation, photos, and methodologies are listed in the respective project folder.

| Project | Description |
|---|---|
| Coming soon | - |
