# SOC Homelab — Architecture Overview

## Project Purpose

This project is a home Security Operations Center (SOC) lab built to simulate a real-world threat detection and incident response environment. The lab replicates a basic corporate network consisting of a monitored Windows endpoint, a SIEM server, and an attack machine. The purpose is to develop hands-on experience in attack simulation, log analysis, alert triage, and incident documentation, core skills required for SOC Analyst roles. All activity is fully contained within an isolated virtual network with no connectivity to the internet or host network.

## Environment Summary

The lab consists of three virtual machines running on VMware Workstation. Each machine serves a distinct role in the SOC workflow:

- **Ubuntu Server (192.168.100.10)** -- SIEM server running Wazuh, responsible for collecting and analyzing security logs from monitored endpoints
- **Windows 11 Home (192.168.100.20)** -- Target endpoint simulating a corporate workstation, monitored by a Wazuh agent
- **Kali Linux (192.168.100.30)** -- Attack machine used to simulate threat actor behavior against the Windows endpoint

## Network Design

![Network Diagram](../images/network-diagram.png)

All three virtual machines are connected through a VMware LAN Segment configured as a fully isolated internal network using the subnet **192.168.100.0/24**. The LAN Segment has no NAT, no DHCP, and no routing to the Internet or the host machine's physical network. Each VM is assigned a static IP address to ensure consistent communication between machines. For a full breakdown of IP assignments, see [Static IP Configuration](static-ip-config.md).

Traffic flow in the lab operates in two directions. Attack traffic flows from Kali Linux toward the Windows 11 endpoint, simulating a threat actor targeting a corporate workstation. Log and alert data flows from the Wazuh agent on Windows 11 to the Wazuh manager on Ubuntu Server, where it is processed and made visible on the web-based Wazuh dashboard.

## Machine Roles & Responsibilities

### Ubuntu Server — SIEM (192.168.100.10)
Ubuntu Server hosts the full Wazuh stack, including the Wazuh Manager, Wazuh Indexer, and Wazuh Dashboard. The Wazuh Manager receives security logs forwarded by agents installed on monitored endpoints, processes them against detection rules, and generates alerts for suspicious activity. The dashboard is accessible via browser at `https://192.168.100.10` from the Windows VM. Ubuntu was chosen for its stability, low resource utilization, and widespread use in the industry. Full installation details are documented in [Ubuntu Server Setup](../setup/ubuntu-setup.md) and [Wazuh Setup](../setup/wazuh-setup.md).

### Windows 11 Home — Target Endpoint (192.168.100.20)
Windows 11 Home serves as the simulated corporate workstation and primary attack target in the lab. Two local user accounts are configured, a standard user account (`j.doe`) representing a regular employee, and an administrator account (`admin`) representing a privileged user. Sysmon is installed alongside the Wazuh agent to generate more detailed, higher-quality system logs, including process creation events, network connections, and file system changes that Windows Event Logs alone would not capture. Several security controls have been intentionally weakened for lab purposes to allow for incoming traffic from the Kali Linux machine, including disabling Windows Defender real-time protection, disabling the Windows Firewall, enabling RDP, and setting weak passwords on user accounts. Full setup details are documented in [Windows 11 Setup](../setup/windows11-setup.md).

### Kali Linux — Attack Machine (192.168.100.30)
Kali Linux serves as the simulated threat actor machine. It is used to perform attack exercises against the Windows 11 endpoint, such as network scanning, brute force attacks, and exploitation attempts. No Wazuh agent is installed on Kali, as it is the source of attacks rather than a monitored endpoint. Kali has no special configuration beyond static IP assignment and standard package updates. Full setup details are documented in [Kali Linux Setup](../setup/kali-setup.md).

## Security Monitoring Stack

The monitoring pipeline works as follows. The Wazuh agent installed on Windows 11 continuously collects Windows Event Logs and Sysmon logs from the endpoint. These logs are forwarded in real time over the isolated LAN Segment to the Wazuh Manager running on Ubuntu Server (192.168.100.10). The Wazuh Manager processes incoming logs against its built-in detection ruleset and generates alerts for suspicious or noteworthy activity. All alerts and agent telemetry are visible through the Wazuh Dashboard, which is accessible through HTTPS via browser from the Windows 11 VM. This setup simulates launching an attack from Kali, then pivoting to the Windows 11 machine to investigate the resulting alerts in the Wazuh dashboard, replicating a SOC detection and investigation workflow. Full details on the monitoring stack are documented in [Wazuh Agent Setup](../setup/wazuh-agent-setup.md) and [Sysmon Setup](../setup/sysmon-setup.md).

## Design Decisions & Rationale

**Why LAN Segment over NAT:**
A LAN Segment provides complete network isolation between the VMs and the outside world. NAT would have given the VMs internet access through the host machine, which introduces unnecessary risk when running attack tools and intentionally vulnerable configurations. The LAN Segment ensures all attack activity is fully contained and cannot affect the host network or any external systems.

**Why Wazuh over other SIEMs:**
Wazuh is free, open source, and widely deployed in real enterprise environments, making it directly relevant to SOC job roles. Compared to alternatives like Splunk, which requires significant resources and licensing for full functionality, Wazuh provides a much more complete experience, including log collection, alerting, and a dashboard within the hardware constraints of a homelab. It also has strong documentation and community support.

**Why Sysmon was added on top of the base Wazuh agent:**
The default Windows Event Logs captured by the Wazuh agent provide limited visibility into endpoint activity. Sysmon helps to improve the system log quality by capturing detailed process creation events, parent-child process relationships, network connection attempts, and file creation events. This additional telemetry is essential for detecting and investigating the kinds of attacks simulated in this lab and reflects a real environment, where Sysmon is commonly deployed alongside SIEM agents.

**Why Windows was intentionally weakened:**
Out of the box, Windows 11 blocks most attack techniques through Defender, the firewall, and strong default configurations. Since the purpose of the lab is to simulate attacks to create telemetry and practice detection, these controls were selectively disabled to allow a greater attack scope and generate meaningful high-value alerts. This is acceptable in isolated lab environments, as all changes are contained within a VM that has no connectivity outside the LAN Segment to the open Internet.

## Known Limitations

- Only a single Windows endpoint is monitored. A real SOC environment would monitor multiple endpoints simultaneously.
- No Kali Linux Wazuh agent is deployed, meaning attacker-side activity is not logged or correlated.
- No network-level monitoring is in place. There is no firewall VM such as pfSense or OPNsense, meaning there is no visibility into network traffic between machines beyond what endpoint logs capture.
- No Active Directory environment exists yet, limiting the ability to simulate AD-based attacks which are common in real corporate environments.
- Windows is running unactivated which restricts access to some built-in management tools.
- The lab currently simulates a flat network with no segmentation beyond the single LAN Segment.

## Future Improvements

- **pfSense or OPNsense firewall VM** — Add network-level visibility, traffic monitoring, and segmentation between the attacker and target networks
- **Windows Server with Active Directory** — Simulate a domain environment to practice AD-based attacks and detections such as pass-the-hash, Kerberoasting, and privilege escalation
- **Additional Windows endpoints** — Add more target machines to simulate lateral movement across multiple workstations
- **Wazuh agent on Kali** — Deploy an agent on the attack machine to correlate attacker-side activity with defender-side alerts
- **Custom Sysmon configuration** — Implement a community Sysmon config such as the SwiftOnSecurity ruleset to further improve detection coverage
- **Vulnerability scanner** — Integrate a tool like OpenVAS or Nessus to add vulnerability assessment exercises to the lab
