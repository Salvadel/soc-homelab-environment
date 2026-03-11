# SOC Homelab — Architecture Overview

## Project Purpose

This project is designed as a home Security Operations Center (SOC) lab, which will be used to simulate the environment of a real-world threat detection and response environment. This will be achieved by creating a simple corporate network with a monitored Windows endpoint, a SIEM server, a SOAR automation server, a firewall, and an attack machine. This will be used to gain experience in the field of attack simulation, which is critical for those wishing to work as SOC Analysts. All attacks will be fully contained within the environment, which will be done with an isolated virtual network and controlled internet access with pfSense.

## Environment Summary

The lab consists of five virtual machines running on VMware Workstation. Each machine serves a distinct role in the SOC-lab:

- **pfSense (192.168.100.1)** - Firewall and router sitting at the edge of the network, managing all traffic between the internal LAN Segment and the internet
- **Ubuntu Server - SIEM (192.168.100.10)** - SIEM server running Wazuh, responsible for collecting and analyzing security logs from monitored endpoints
- **Windows 11 Home (192.168.100.20)** - Target endpoint simulating a corporate workstation, monitored by a Wazuh agent
- **Kali Linux (192.168.100.30)** - Attack machine used to simulate threat actor behavior against the Windows endpoint
- **Ubuntu Server - SOAR (192.168.100.40)** - SOAR server running Shuffle and TheHive, responsible for automated alert triage, case management, and analyst notifications via Slack

## Network Design

![Network Diagram](../images/network-diagram.png)

All five virtual machines are connected through a VMware LAN Segment using the subnet **192.168.100.0/24**. pfSense sits at the network perimeter with two network adapters - a WAN adapter connected to VMware NAT for internet access, and a LAN adapter connected to the internal segment. All VMs use pfSense at 192.168.100.1 as their default gateway, meaning all internet-bound traffic is routed through pfSense before reaching the outside network. Internal VM to VM traffic stays on the LAN Segment and bypasses pfSense entirely. Each VM is assigned a static IP address to ensure consistent communication between machines. For a full breakdown of IP assignments, see [Static IP Configuration](static-ip-configuration.md).

Traffic flow in the lab operates across three paths. Attack traffic flows from Kali Linux toward the Windows 11 endpoint, simulating a threat actor targeting a corporate workstation. Log and alert data flows from the Wazuh agent on Windows 11 to the Wazuh Manager on the Ubuntu Server - SIEM, where it is processed and triggers automated response workflows. Automation and notification data flows from Wazuh to Shuffle on the Ubuntu Server - SOAR, which creates cases in TheHive and sends notifications to the analyst via Slack. For a detailed view of how data moves through the full pipeline, see the [Data Flow Diagram](../images/data-flow-diagram.png).

## Machine Roles & Responsibilities

### pfSense - Firewall / Router (192.168.100.1)
pfSense acts as the network perimeter firewall and router for the lab environment. It sits between the VMware NAT adapter and the internal LAN Segment, managing all traffic entering and leaving the network. pfSense logs all traffic passing through it, providing network-level visibility that complements the endpoint-level visibility provided by Wazuh. This mirrors how real SOC environments layer network and endpoint monitoring for more complete detection coverage. Full installation details are documented in [pfSense Setup](../setup/pfsense-setup.md).

### Ubuntu Server - SIEM (192.168.100.10)
Ubuntu Server - SIEM hosts the full Wazuh stack, including the Wazuh Manager, Wazuh Indexer, and Wazuh Dashboard. The Wazuh Manager receives security logs forwarded by agents installed on monitored endpoints, processes them against detection rules, and generates alerts for suspicious activity. The dashboard is accessible via browser at `https://192.168.100.10` from the Windows VM. Ubuntu was chosen for its stability, low resource utilization, and widespread use in the industry. Full installation details are documented in [Ubuntu Server Setup](../setup/siem-server-setup.md) and [Wazuh Setup](../setup/wazuh-setup.md).

### Windows 11 Home - Target Endpoint (192.168.100.20)
Windows 11 Home serves as the simulated corporate workstation and primary attack target in the lab. Two local user accounts are configured, a standard user account (`j.doe`) representing a regular employee, and an administrator account (`admin`) representing a privileged user. Sysmon is installed alongside the Wazuh agent to generate more detailed, higher-quality system logs, including process creation events, network connections, and file system changes that Windows Event Logs alone would not capture. Several security controls have been intentionally weakened for lab purposes to allow for incoming traffic from the Kali Linux machine, including disabling Windows Defender real-time protection, disabling the Windows Firewall, enabling RDP, and setting weak passwords on user accounts. Full setup details are documented in [Windows 11 Setup](../setup/windows11-setup.md).

### Kali Linux - Attack Machine (192.168.100.30)
Kali Linux serves as the simulated threat actor machine. It is used to perform attack exercises against the Windows 11 endpoint, such as network scanning, brute force attacks, and exploitation attempts. No Wazuh agent is installed on Kali, as it is the source of attacks rather than a monitored endpoint. Kali has no special configuration beyond static IP assignment and standard package updates. Full setup details are documented in [Kali Linux Setup](../setup/kali-setup.md).

### Ubuntu Server - SOAR (192.168.100.40)
Ubuntu Server - SOAR runs the full SOAR stack for the lab, including Shuffle for automation workflows and TheHive for case management. When Wazuh generates an alert, it triggers a Shuffle webhook, which automatically creates a case in TheHive and sends a Slack notification to the analyst. This automates the first stage of alert triage and replicates the kind of SOAR pipeline used in real SOC environments. Full installation details are documented in [Ubuntu Server — SOAR Setup](../setup/soar-server-setup.md), [Shuffle Setup](../setup/shuffle-setup.md), and [TheHive Setup](../setup/thehive-setup.md).

## Security Monitoring Stack

The monitoring and response pipeline works as follows. The Wazuh agent installed on Windows 11 continuously collects Windows Event Logs and Sysmon logs from the endpoint. These logs are forwarded in real time over the LAN Segment to the Wazuh Manager running on Ubuntu Server — SIEM (192.168.100.10). The Wazuh Manager processes incoming logs against its built-in detection ruleset and generates alerts for suspicious or noteworthy activity. When a qualifying alert fires, a webhook triggers Shuffle on Ubuntu Server - SOAR (192.168.100.40), which runs an automated workflow to create a case in TheHive and send a Slack notification to the analyst. The analyst then investigates the case through the TheHive dashboard and cross references findings in the Wazuh dashboard. This setup replicates a complete SOC detection and response workflow - from attack through detection, automation, case creation, and investigation. Full details on the monitoring stack are documented in [Wazuh Agent Setup](../setup/wazuh-agent-setup.md) and [Sysmon Setup](../setup/sysmon-setup.md).

## Design Decisions & Rationale

**Why pfSense as the network firewall:**
pfSense is a free, open source firewall platform that is widely used in enterprise environments. Adding pfSense to the lab introduces a real network perimeter, firewall rule management, and traffic logging that complements the endpoint-level detection provided by Wazuh. It also provides the controlled internet access required for the Ubuntu Server - SOAR to function fully while keeping attack simulation traffic isolated within the internal LAN Segment.

**Why a dedicated SOAR server separate from the Wazuh server:**
Keeping the detection layer and response layer on separate servers mirrors how real SOC environments separate their tooling. It also prevents resource contention - Wazuh and TheHive each have significant memory requirements, and separating them ensures both perform reliably during active exercises. The separation also means that a failure or reboot of one server does not take down the entire SOC pipeline.

**Why Wazuh over other SIEMs:**
Wazuh is free, open source, and widely deployed in real environments. Compared to alternatives like Splunk, which requires significant resources and licensing for full functionality, Wazuh provides a much more complete experience, including log collection, alerting, and a dashboard within the hardware constraints of a homelab. It also has strong documentation and community support.

**Why Sysmon was added on top of the base Wazuh agent:**
The default Windows Event Logs captured by the Wazuh agent provide limited visibility into endpoint activity. Sysmon improves log quality by capturing detailed process creation events, parent-child process relationships, network connection attempts, and file creation events. This additional telemetry is essential for detecting and investigating the kinds of attacks simulated in this lab and reflects a real environment where Sysmon is commonly deployed alongside SIEM agents.

**Why Windows was intentionally weakened:**
Out of the box, Windows 11 blocks most attack techniques through Defender, the firewall, and strong default configurations. Since the purpose of the lab is to simulate attacks to create telemetry and practice detection, these controls were selectively disabled to allow a greater attack scope and generate meaningful high-value alerts. This is acceptable in isolated lab environments as all attack activity is contained within the LAN Segment with no direct path to the open internet.

**Why Slack for analyst notifications:**
Slack is free, widely used in real SOC and IT environments, and has native integration with Shuffle. Using Slack for alert notifications mirrors how many real SOC teams handle analyst alerting and mirrors a tool the analyst would already be familiar with in a professional environment.

## Known Limitations

- Only a single Windows endpoint is monitored. A real SOC environment would monitor multiple endpoints simultaneously.
- No Kali Linux Wazuh agent is deployed, meaning attacker-side activity is not logged or correlated.
- No Active Directory environment exists yet, limiting the ability to simulate AD-based attacks, which are common in real corporate environments.
- Windows is running unactivated, which restricts access to some built-in management tools.
- The lab currently simulates a flat network with no segmentation between the attacker and the monitored endpoints beyond pfSense firewall rules.

## Future Improvements

- **Windows Server with Active Directory** — Simulate a domain environment to practice AD-based attacks and detections such as pass-the-hash, Kerberoasting, and privilege escalation
- **Additional Windows endpoints** — Add more target machines to simulate lateral movement across multiple workstations
- **Wazuh agent on Kali** — Deploy an agent on the attack machine to correlate attacker-side activity with defender-side alerts
- **Custom Sysmon configuration** — Implement a community Sysmon config such as the SwiftOnSecurity ruleset to improve detection coverage further
- **Vulnerability scanner** — Integrate a tool like OpenVAS or Nessus to add vulnerability assessment exercises to the lab
- **Network segmentation** — Add a dedicated attacker network segment to force all attack traffic through pfSense firewall rules, more closely mirroring a real perimeter defense scenario
