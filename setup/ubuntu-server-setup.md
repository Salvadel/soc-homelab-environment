# Ubuntu Server Setup

This document covers the installation and configuration of the Ubuntu Server virtual machine in the SOC homelab. Ubuntu Server serves as the SIEM host, running the full Wazuh stack including the Wazuh Manager, Wazuh Indexer, and Wazuh Dashboard. Full Wazuh installation details are documented separately in [Wazuh Setup](wazuh-setup.md).

## VM Specifications

| Property | Value |
|---|---|
| Operating System | Ubuntu Server 24 |
| RAM | 4GB |
| CPUs | 2 |
| Storage | 80GB |
| Network Adapter | LAN Segment (Isolated) |
| IP Address | 192.168.100.10 |
| Role | SIEM Server (Wazuh) |

## Installation

Ubuntu Server was installed as a virtual machine in VMware Workstation using the official Ubuntu Server ISO. During installation default settings were accepted with the exception of the network configuration which was set to the isolated LAN Segment after installation was complete. No desktop environment was installed — Ubuntu Server runs headless via terminal only, which reduces resource usage and reflects how servers are typically managed in real enterprise environments. The official Ubuntu Server ISO can be downloaded from the [Ubuntu official download page](https://ubuntu.com/download/server).

Storage was allocated at 80GB, more generously than the other VMs, to accommodate Wazuh log and alert data accumulation over time as lab exercises are performed.

### Ubuntu Server Terminal

The screenshot below confirms the Ubuntu Server VM is fully installed and operational.

![Ubuntu Server Terminal](../images/ubuntu-terminal.png)

## Network Configuration

A static IP address was manually assigned to the Ubuntu Server VM to ensure consistent addressing within the isolated LAN Segment. This is critical for Wazuh agent-to-manager communication — all agents on the Windows 11 and Kali Linux VMs are configured to point to this fixed IP address. No default gateway or DNS was configured as the LAN Segment has no routing to external networks.

### Static IP Assignment

| Property | Value |
|---|---|
| IP Address | 192.168.100.10 |
| Subnet Mask | 255.255.255.0 |
| Gateway | None |
| DNS | None |

The screenshot below shows the output of `ip a` confirming the static IP address has been correctly assigned to the Ubuntu Server VM.

![Ubuntu IP Configuration](../images/ubuntu-ip-config.png)

## System Update

After installation, the system package list and all installed packages were updated to ensure the latest libraries and security patches are in place before Wazuh installation.
```bash
sudo apt update && sudo apt upgrade -y
```

## Wazuh Services

The full Wazuh stack is installed and running on Ubuntu Server. All three Wazuh services are configured to start automatically on boot. Full installation details are documented in [Wazuh Setup](wazuh-setup.md).

To start Wazuh services manually after booting:
```bash
sudo systemctl start wazuh-manager
sudo systemctl start wazuh-indexer
sudo systemctl start wazuh-dashboard
```

The screenshot below confirms all three Wazuh services are active and running.

![Wazuh Services Running](../images/ubuntu-wazuh-running.png)

## Connectivity Verification

After static IP assignment, connectivity to both other VMs on the LAN Segment was verified using ping to confirm the isolated network is functioning correctly.

### Ubuntu Server → Windows 11
```bash
ping 192.168.100.20
```

![Ping Test Ubuntu to Windows](../images/ping-test-server-to-windows.png)

### Ubuntu Server → Kali Linux
```bash
ping 192.168.100.30
```

![Ping Test Server to Kali](../images/ping-test-server-to-kali.png)

## Configuration Notes

- Ubuntu Server runs headless with no desktop environment installed, reducing RAM and CPU overhead and leaving more resources available for the Wazuh stack
- 80GB storage was allocated specifically to accommodate Wazuh log data accumulation over time, as lab exercises are performed - this is the most storage-intensive VM in the lab
- All Wazuh services are set to start automatically on boot via systemctl enable, meaning the SIEM is fully operational as soon as the VM boots without manual intervention
- The Wazuh dashboard is accessible via browser from the Windows 11 VM at `https://192.168.100.10`
