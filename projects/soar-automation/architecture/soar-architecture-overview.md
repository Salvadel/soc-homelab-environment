# SOAR Architecture Overview

This document explains the design decisions behind the SOAR automation project: why each technology was chosen, how this project's infrastructure connects to the core lab, and how alerts flow from detection to analyst notification. Step-by-step installation and configuration for each component is documented separately in the [setup](../setup/) folder.

This project builds on top of the core lab, which is assumed to already be fully built and operational.

## Network Diagram

![SOAR Automation Network Diagram](../images/soar-automation-diagram.png)

This project added a new dedicated network segment, SOC-Lab-SOAR (192.168.40.0/24), to the existing pfSense VM. This required adding a 5th network adapter and interface (em5) to pfSense, expanding it beyond the 4 interfaces documented in the core lab. The core lab's own documentation is treated as a snapshot of the lab at the time that phase was completed; this project's documentation is the authoritative source for the network expansion described here.

## Data Flow Diagram

![SOAR Data Flow Diagram](../images/soar-data-flow-diagram.png)

This diagram shows how a single Wazuh alert moves through the automation pipeline: Wazuh forwards a qualifying alert to Shuffle via webhook, Shuffle queries VirusTotal and AbuseIPDB in parallel to enrich the alert with threat intelligence, Shuffle creates a case in TheHive using the enriched data, and Shuffle sends a Slack notification referencing the newly created case. Full technical detail for each step is documented in [Shuffle Setup](../setup/shuffle-setup.md).

## Project Topology Summary

| Device / Interface | Role | VMware LAN Segment | Subnet | Static IP | Gateway |
|---|---|---|---|---|---|
| pfSense (LAN40) | Router / Firewall (project expansion) | SOC-Lab-SOAR | 192.168.40.0/24 | 192.168.40.1 | N/A |
| Ubuntu Server (SOAR) | SOAR Server (Shuffle / TheHive) | SOC-Lab-SOAR | 192.168.40.0/24 | 192.168.40.40 | 192.168.40.1 |

## Why a Dedicated SOAR Segment

The SOAR host was placed on its own dedicated network segment rather than sharing the existing SIEM segment for the following reason:

**Isolation** - Keeping the SOAR stack on its own segment isolates it from the monitored segments (SIEM, Windows, Kali), so the automation infrastructure itself is not exposed on the same network as the systems it monitors and responds to.

## Why Ubuntu Server (SOAR Host)

Ubuntu Server was chosen to host the SOAR stack for the same reasons it was chosen for the core lab's SIEM host:

**Free and Open Source** - Ubuntu Server carries no licensing cost, keeping the project free to build and reproduce.

**Enterprise Relevance** - Ubuntu is one of the most widely deployed Linux distributions in production server environments, making it directly relevant to real-world SOC and infrastructure roles.

**Lightweight and Headless** - Running Ubuntu Server without a desktop environment reduces resource overhead, which matters here given TheHive, Cassandra, Elasticsearch, and Shuffle's Docker containers all run concurrently on this single VM.

## Why Shuffle

Shuffle was chosen as the SOAR platform for this project for the following reasons:

**Open Source** - Shuffle is completely free and open source with no licensing restrictions, making it suitable for homelab use without cost.

**Visual Workflow Builder** - Shuffle provides a drag-and-drop workflow builder that makes it straightforward to build and understand automation logic without writing code.

**Native Integrations** - Shuffle has built-in integrations for Wazuh, TheHive, VirusTotal, AbuseIPDB, and Slack, covering every tool in this project's pipeline without requiring custom development.

**Real World Relevance** - Shuffle is used in real SOC environments and demonstrates practical SOAR skills directly applicable to SOC analyst and engineer roles.

## Why TheHive

TheHive was chosen as the case management platform for this project for the following reasons:

**Open Source** - TheHive is free and open source with a Community license available for homelab use. It provides enterprise-grade case management capabilities without licensing costs.

**SOAR Integration** - TheHive integrates natively with Shuffle, allowing cases to be created automatically from Wazuh alerts without manual intervention.

**Real World Relevance** - TheHive is widely used in real SOC environments and is directly relevant to SOC analyst job roles. Experience with TheHive translates directly to real-world skills.

**Structured Investigation Workflow** - TheHive provides a structured case management workflow including tasks, observables, and response actions that mirror how real SOC teams manage incidents.
