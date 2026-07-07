# Architecture Overview

This document explains the design decisions behind the SOC homelab: why each device and technology was chosen, how the network is structured and addressed, and how all components communicate with each other. Step by step installation and configuration for each component is documented separately in the [setup](../setup/) folder.

## Network Diagram

![Core Lab Network Diagram](../images/core-lab-diagram.png)

The Firewall and Wireless Gateway icons together represent the single pfSense VM, which handles both firewall and routing across four interfaces: one WAN facing the ISP, and three LAN interfaces, one per segment. Each of the three devices sits on its own isolated segment and reaches the others only by routing through pfSense.

| Device | Role | VMware LAN Segment | Subnet | Static IP | Gateway |
|---|---|---|---|---|---|
| pfSense (WAN) | Router / Firewall | NAT | Host assigned | DHCP via VMware NAT | N/A |
| pfSense (LAN10) | Router / Firewall | SOC-Lab-SIEM | 192.168.10.0/24 | 192.168.10.1 | N/A |
| pfSense (LAN20) | Router / Firewall | SOC-Lab-Windows | 192.168.20.0/24 | 192.168.20.1 | N/A |
| pfSense (LAN30) | Router / Firewall | SOC-Lab-Kali | 192.168.30.0/24 | 192.168.30.1 | N/A |
| Ubuntu Server | SIEM Server (Wazuh) | SOC-Lab-SIEM | 192.168.10.0/24 | 192.168.10.10 | 192.168.10.1 |
| Windows 11 | Target Endpoint | SOC-Lab-Windows | 192.168.20.0/24 | 192.168.20.20 | 192.168.20.1 |
| Kali Linux | Attack Machine | SOC-Lab-Kali | 192.168.30.0/24 | 192.168.30.30 | 192.168.30.1 |

## Why VMware Workstation Pro

VMware Workstation Pro was chosen as the hypervisor for this lab for the following reasons:

**Industry Use** - VMware is widely deployed in enterprise environments, making experience with it directly relevant to IT and security roles.

**Resource Efficiency** - VMware Workstation Pro manages system resources more efficiently than several alternative hypervisors, which matters in a homelab where hardware is shared across four running VMs simultaneously.

**Multi-VM Management** - VMware Workstation Pro provides strong tooling for managing, snapshotting, and networking multiple VMs at once, which suits a lab built around several interconnected machines.

## Why pfSense

pfSense was chosen as the network firewall and router for this lab for the following reasons:

**Open Source** - pfSense CE is completely free and open source with no licensing restrictions, making it suitable for homelab use without cost.

**Enterprise Relevance** - pfSense is widely deployed in real enterprise environments, making it directly relevant to SOC and network engineering roles.

**Network Segmentation** - pfSense allows each lab device to sit on its own isolated LAN segment with its own gateway, mirroring how real enterprise networks separate systems by function and trust level.

**Controlled Internet Access** - pfSense provides controlled internet access through VMware NAT while keeping each internal LAN segment isolated from the host machine's physical network and from each other.

## Why Ubuntu Server

Ubuntu Server was chosen to host the Wazuh SIEM stack for the following reasons:

**Free and Open Source** - Ubuntu Server carries no licensing cost, keeping the lab free to build and reproduce.

**Enterprise Relevance** - Ubuntu is one of the most widely deployed Linux distributions in production server environments, making it directly relevant to real world SOC and infrastructure roles.

**Lightweight and Headless** - Running Ubuntu Server without a desktop environment reduces resource overhead, leaving more system resources available for the Wazuh stack itself.

## Why Wazuh

Wazuh was chosen as the SIEM platform for this lab over alternatives such as Splunk and Elastic SIEM for the following reasons:

**Cost** - Wazuh is free and open source, with no licensing restrictions. Splunk's free tier limits how much data can be collected per day, which is not ideal for a lab generating endpoint telemetry. Elastic Stack requires significant configuration overhead to reach capabilities Wazuh provides out of the box.

**Enterprise Relevance** - Wazuh is widely deployed in production environments, making it directly relevant to industry standards. Experience with Wazuh reflects real world skills used by SOC and security professionals.

** All-in-One Stack** - Wazuh provides a complete SIEM solution, including log collection, threat detection, alerting, and a dashboard in a single installation. This reduces setup complexity and maintenance overhead.

**Resource Efficiency** - Wazuh generally runs more efficiently with fewer system resources than Elastic or Splunk, which matters in a homelab where system resources are tightly controlled.

**Community and Documentation** - Wazuh has extensive official documentation and an active community, making troubleshooting and learning straightforward.

## Why Windows 11

Windows 11 Home was chosen as the target endpoint for the following reasons:

**Realistic Corporate Target** - Windows remains the dominant operating system on corporate endpoints, making it the most realistic choice for a target machine in SOC focused exercises.

**Free and Accessible** - Windows 11 is easy to obtain and install for lab use through the official Microsoft Media Creation Tool, without additional cost for a personal, non production lab.

**Resource Light** - Windows 11 Home runs acceptably within the lab's shared resource budget, without requiring the additional overhead of a Windows Server edition that this lab does not otherwise need.

## Why Kali Linux

Kali Linux was chosen as the attack machine for the following reasons:

**Industry Standard** - Kali Linux is the most widely recognized penetration testing distribution, making experience with it directly relevant to offensive security and red team roles.

**Prebuilt Toolset** - Kali ships with an extensive collection of offensive security tools preinstalled, removing the overhead of manually sourcing and configuring individual tools.

**Free and Open Source** - Kali Linux carries no licensing cost and is freely available as a prebuilt VMware image, simplifying deployment.

## Network Segmentation Design

The lab is intentionally divided into three isolated LAN segments, SOC-Lab-SIEM, SOC-Lab-Windows, and SOC-Lab-Kali, rather than placing all devices on a single flat network. This design mirrors how real enterprise networks segment systems by function and trust level, for example separating monitoring infrastructure, general endpoints, and higher risk systems into distinct network zones. Each segment connects to pfSense through its own dedicated interface, allowing traffic between segments to be observed, controlled, and eventually restricted as the lab's firewall rules are hardened in a future project.

## Static IP Addressing Design

Static IP addresses, configured locally on each guest operating system, were used throughout the lab instead of DHCP reservations on pfSense. This provides more reliable and predictable addressing for Wazuh agent-to-manager communication, since agents are configured to report to a fixed Wazuh Manager IP address. Consistent addressing also simplifies documentation, troubleshooting, and firewall rule creation, since every device's address is fixed and known in advance rather than subject to lease renewal or DHCP server availability.
