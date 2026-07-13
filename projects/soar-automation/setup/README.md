# Setup

This folder contains step-by-step installation and configuration guides for every component in the SOAR automation project. Each document is scoped to a single component so it stays focused and reusable if that component is ever redeployed on its own. Rationale for why each technology was chosen is documented separately in the Architecture Overview for this project; these guides cover the "how," not the "why."

## Recommended Install Order

Some components depend on others being in place first; follow this order when building this project from scratch:

1. [Ubuntu Server Setup (SOAR)](ubuntu-soar-setup.md) - Installs and configures the Ubuntu Server VM that hosts the SOAR stack, including static IP assignment on a new dedicated LAN segment. Covers the base operating system only. This must be done first, since Shuffle and TheHive both run on top of this VM.
2. [TheHive Setup](thehive-setup.md) - Installs TheHive, Cassandra, and Elasticsearch for case management, and creates the organisation and integration user Shuffle later uses to create cases automatically. Must be completed before finishing the Shuffle TheHive integration step, since Shuffle needs the API key generated here.
3. [Shuffle Setup](shuffle-setup.md) - Installs Docker and Shuffle, then builds the automation workflow that receives Wazuh alerts, enriches them with VirusTotal and AbuseIPDB, creates a case in TheHive, and sends a Slack notification. Requires the Ubuntu Server SOAR host and TheHive to already be set up.

## Component Purpose Summary

| Document | Component | Purpose in the Project |
|---|---|---|
| ubuntu-soar-setup.md | Ubuntu Server | Base OS hosting the Shuffle and TheHive stack |
| thehive-setup.md | TheHive | Case management platform, receives and tracks incidents created from Wazuh alerts |
| shuffle-setup.md | Shuffle | SOAR automation platform, connects Wazuh, IOC enrichment, TheHive, and Slack into one pipeline |

## Other Notes

- The Ubuntu Server SOAR host uses a static IP configured locally on the guest OS, on a new dedicated LAN segment separate from the core lab's existing segments
- Shuffle's Docker Compose configuration required several manual environment variable changes to run correctly on a single-node setup; see the Docker Compose Configuration section in [Shuffle Setup](shuffle-setup.md) for details
- This project assumes the core lab (pfSense, the Wazuh SIEM, and the Windows 11 endpoint) is already fully built and operational; see the core lab's own documentation for that setup
- Several documents reference each other directly (for example, Shuffle Setup links back to TheHive Setup for the integration API key); follow those links if a step assumes something covered in another file
