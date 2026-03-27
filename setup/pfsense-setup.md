# pfSense Setup

This document covers the installation and configuration of the pfSense firewall virtual machine in the SOC homelab. pfSense sits at the network perimeter, managing all traffic between the internal LAN Segment and the internet via VMware NAT. It provides network level visibility through traffic logging that complements the endpoint level detection provided by Wazuh.

## Why pfSense

pfSense was chosen as the network firewall for this lab for the following reasons:

**Open Source** - pfSense CE is completely free and open source with no licensing restrictions, making it suitable for homelab use without cost.

**Enterprise Relevance** - pfSense is widely deployed in real enterprise environments, making it directly relevant to SOC and network engineering roles. Experience with pfSense translates directly to real-world skills.

**Network Visibility** - pfSense logs all traffic passing through it, providing network-level evidence that complements the endpoint-level logs collected by Wazuh. This mirrors how real SOC environments layer network and endpoint monitoring for more complete detection coverage.

**Controlled Internet Access** - pfSense provides controlled internet access through VMware NAT while keeping the internal LAN Segment isolated from the host machine's physical network.

## VM Specifications

| Property | Value |
|---|---|
| Operating System | pfSense CE 2.7.2 |
| RAM | 1GB |
| CPUs | 1 |
| Storage | 20GB |
| Network Adapter 1 | NAT (WAN) |
| Network Adapter 2 | LAN Segment (LAN) |
| IP Address | 192.168.100.1 |
| Role | Firewall / Router |

The screenshot below shows the pfSense VM hardware configuration in VMware, including both network adapters.

![pfSense VMware Configuration](../images/firewall-vmware.png)

## Installation

pfSense CE 2.7.2 was installed as a virtual machine in VMware Workstation using the official pfSense CE ISO. The official pfSense CE ISO can be downloaded from [https://www.pfsense.org/download](https://www.pfsense.org/download).

During installation, the following options were selected:

| Option | Value |
|---|---|
| Partition Scheme | GPT |
| Filesystem | UFS |
| All other settings | Default |

## Interface Assignment

On first boot, pfSense prompts for interface assignment. The following assignments were made:

| Interface | Adapter | Purpose |
|---|---|---|
| WAN | em0 (NAT) | Internet access via VMware NAT |
| LAN | em1 (LAN Segment) | Internal lab network |

When prompted during interface assignment:
- VLANs: `n`
- WAN interface: `em0`
- LAN interface: `em1`

The LAN IP address was set to `192.168.100.1` with subnet mask `255.255.255.0`.

## Initial Configuration Wizard

On first login to the pfSense web dashboard, the setup wizard was completed with the following configuration:

### General Information

| Field | Value |
|---|---|
| Hostname | pfsense |
| Domain | soc.local |
| Primary DNS | 8.8.8.8 (Google) |
| Secondary DNS | 1.1.1.1 (Cloudflare) |
| Override DNS | Enabled |

### WAN Configuration
Left as DHCP - VMware NAT automatically assigns the WAN IP address.

### LAN Configuration
Confirmed LAN IP address as `192.168.100.1` with subnet mask `255.255.255.0`.

### Admin Password
The default admin password was changed from `pfsense` to a secure password during the wizard.

## Accessing the Dashboard

The pfSense web dashboard is accessible from the Windows 11 VM browser at:
```
https://192.168.100.1
```

A self-signed SSL certificate is used by default, which causes the browser to display a security warning on first access. This is expected behavior - proceed by clicking **Advanced > Proceed** to access the dashboard.

The screenshot below shows the pfSense dashboard and interface overview, confirming WAN and LAN interfaces are active, and the firewall is operational.

![pfSense Dashboard](../images/pfsense-dashboard.png)

## Connectivity Verification

After pfSense was fully configured, connectivity was verified from all VMs on the LAN Segment. For full network connectivity verification across all critical lab communication paths, see [Static IP Configuration](../architecture/static-ip-configuration.md).

The following ping test confirms pfSense is reachable as the default gateway from the Windows 11 VM and that internet routing through pfSense is working correctly:
```powershell
ping 192.168.100.1
ping 8.8.8.8
```

![pfSense Connectivity Test](../images/ping-test-internet.png)

## Configuration Notes

- pfSense must always be the first VM booted and the last VM shut down - all other VMs depend on pfSense for gateway routing and internet access
- The WAN interface receives its IP automatically from VMware NAT - no static WAN IP is configured
- DNS queries from all VMs are forwarded upstream through pfSense to 8.8.8.8 and 1.1.1.1
- The pfSense dashboard uses a self-signed SSL certificate by default - the browser security warning on first access is expected and can be safely bypassed within the lab environment
- The default admin password was changed from `pfsense` during the initial setup wizard
- pfSense logs all traffic passing through it, providing network-level visibility that complements the endpoint-level detection provided by Wazuh
- Full pfSense documentation is available at [https://docs.netgate.com/pfsense/en/latest](https://docs.netgate.com/pfsense/en/latest)
