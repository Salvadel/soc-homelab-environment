# SOC Homelab

A home Security Operations Center (SOC) lab designed for simulating real-world threat detection and response scenarios. The lab mimics a basic corporate network infrastructure with a monitored Windows endpoint, SIEM server, firewall, and attack machine, all connected through a pfSense-managed internal network, with additional capabilities layered on top through dedicated projects. The goal is to gain practical knowledge and experience in attack simulation, log analysis, SOAR automation, and incident response, which are critical skills for becoming a SOC Analyst.

This repository is organized into two top-level areas: the **core lab**, a fixed baseline environment (pfSense, Wazuh SIEM, target endpoint, attack machine), and **projects**, self-contained additions that build on top of the core lab over time.

## Where to Start

- **[Core Lab](core-lab/README.md)** - the baseline environment. Start here to build the lab from scratch: pfSense, the Wazuh SIEM, the Windows 11 target endpoint, and the Kali attack machine.
- **[Projects](projects/README.md)** - self-contained additions built on top of the core lab, each documenting its own architecture, setup, and outcomes.

## Current Projects

| Project | Status | Overview |
|---|---|---|
| [SOAR Automation](projects/soar-automation/README.md) | In Progress | Adds security orchestration and automated response on top of the core lab, enriching Wazuh alerts with threat intelligence, creating cases in TheHive, and sending Slack notifications, using Shuffle |
| AWS Wazuh Log Ingestion | In Progress | Documentation not yet available |

## Technologies Used

| Technology | Role |
|---|---|
| VMware Workstation Pro | Hypervisor hosting all lab virtual machines |
| pfSense | Network perimeter firewall and router |
| Windows 11 Home | Target endpoint simulating a corporate workstation |
| Kali Linux | Attack machine used to simulate threat actor behavior |
| Ubuntu Server (SIEM) | Server hosting the full Wazuh stack |
| Wazuh | Open-source SIEM for log collection, alerting, and dashboarding |
| Sysmon | Windows endpoint telemetry enhancement tool |
| Ubuntu Server (SOAR) | Server hosting Shuffle, TheHive, and IOC enrichment integrations |
| Shuffle | Open source SOAR platform for automated alert response workflows |
| TheHive | Open source case management platform for incident investigation |
| Slack | Analyst notification platform integrated with Shuffle |
| VirusTotal | IOC enrichment, IP, hash, and URL reputation lookups |
| AbuseIPDB | IOC enrichment, IP reputation and abuse reporting |

## Repository Structure

```
soc-homelab/
├── README.md
├── core-lab/
│   ├── README.md
│   ├── architecture/
│   ├── setup/
│   └── images/
└── projects/
    ├── README.md
    ├── soar-automation/
    └── siem-log-investigation/
```
