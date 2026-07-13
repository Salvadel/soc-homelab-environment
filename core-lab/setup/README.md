# Setup

This folder contains step-by-step installation and configuration guides for every component in the core SOC homelab. Each document is scoped to a single component so it stays focused and reusable if that component is ever redeployed on its own. Rationale for why each technology was chosen is documented separately in the [Architecture Overview](../architecture/architecture-overview.md), these guides cover the "how," not the "why."

## Recommended Install Order

Some components depend on others being in place first; follow this order when building the lab from scratch:

1. [VMware Setup](vmware-setup.md) - Installs VMware Workstation Pro on the host machine and provides an overview of every VM's resource allocation and network connectivity. This must be done first, since every other VM runs inside VMware.
2. [pfSense Setup](pfsense-setup.md) - Installs and configures pfSense as the lab's router and firewall, establishing the three isolated LAN segments and internet access. Must be completed before any device VM is brought online, since all of them depend on pfSense for gateway routing.
3. [Ubuntu Server Setup](ubuntu-siem-server-setup.md) - Installs and configures the Ubuntu Server VM that later hosts the Wazuh SIEM stack, including static IP assignment. Covers the base operating system only.
4. [Windows 11 Setup](windows11-setup.md) - Installs and configures the Windows 11 VM that serves as the lab's target endpoint, including static IP assignment and user accounts.
5. [Kali Linux Setup](kali-setup.md) - Deploys the Kali Linux VM that serves as the lab's attack machine, including static IP assignment.
6. [Wazuh Setup](wazuh-setup.md) - Installs the full Wazuh SIEM stack (manager, indexer, dashboard) on the Ubuntu Server VM and deploys the Wazuh agent to the Windows 11 endpoint. Requires Ubuntu Server and Windows 11 to already be set up.
7. [Sysmon Setup](sysmon-setup.md) - Installs and configures Sysmon on the Windows 11 endpoint to enhance the detail of logs forwarded to Wazuh. Requires Windows 11 and the Wazuh agent to already be set up and reporting.

## Component Purpose Summary

| Document | Component | Purpose in the Lab |
|---|---|---|
| vmware-setup.md | VMware Workstation Pro | Hypervisor hosting all lab VMs |
| pfsense-setup.md | pfSense | Router and firewall, segments and routes all lab traffic |
| ubuntu-setup.md | Ubuntu Server | Base OS hosting the Wazuh SIEM stack |
| windows-setup.md | Windows 11 | Target endpoint, monitored by Wazuh and Sysmon |
| kali-setup.md | Kali Linux | Attack machine used to simulate threat actor activity |
| wazuh-setup.md | Wazuh | SIEM stack collecting, analyzing, and alerting on security logs |
| sysmon-setup.md | Sysmon | Enhances endpoint telemetry collected from Windows 11 |

## Other Notes

- Every device in the lab uses a static IP configured locally on the guest OS rather than a DHCP reservation; see the [Architecture Overview](../architecture/architecture-overview.md) for the full IP addressing scheme and reasoning
- Several documents reference each other directly (for example, Wazuh Setup links back to Ubuntu Server Setup for prerequisites), follow those links if a step assumes something covered in another file
