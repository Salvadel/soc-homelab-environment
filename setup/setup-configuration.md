# VMware Configuration

This document covers the VMware Workstation configuration for the SOC homelab, including virtual machine hardware specifications, network isolation setup, and security hardening of the VM environment. All three virtual machines are hosted on a single physical machine running VMware Workstation with 32GB RAM.

## Host Machine Specifications

| Property | Value |
|---|---|
| Hypervisor | VMware Workstation |
| Host RAM | 32GB |
| Network Type | LAN Segment (Isolated) |
| Subnet | 192.168.100.0/24 |
| DHCP | Disabled |
| Internet Access | None |

## Network Isolation

All three virtual machines are connected to a VMware **LAN Segment** — an isolated virtual network with no NAT, no DHCP, and no routing to the host machine's physical network or the internet. This ensures all attack simulations and lab activity are fully contained within the virtual environment and cannot affect external systems.

A LAN Segment was chosen over NAT or Bridged networking specifically because it provides complete isolation between the guest VMs and the outside world, which is a critical requirement when running intentionally vulnerable configurations and offensive security tools.

## Virtual Machine Configurations

### Windows 11 Home

The screenshot below shows the Windows 11 VM hardware configuration, including memory, processor allocation, and network adapter assignment to the isolated LAN Segment.

![Windows 11 Configuration](../images/vmware-windows-network.png)

| Property | Value |
|---|---|
| Operating System | Windows 11 Home |
| RAM | 4GB |
| CPUs | 2 |
| Storage | 64GB |
| Network Adapter | LAN Segment |
| IP Address | 192.168.100.20 |
| Role | Target Endpoint |

### Kali Linux

The screenshot below shows the Kali Linux VM hardware configuration, including memory, processor allocation, and network adapter assignment to the isolated LAN Segment.

![Kali Linux Configuration](../images/vmware-kali-network.png)

| Property | Value |
|---|---|
| Operating System | Kali Linux |
| RAM | 4GB |
| CPUs | 2 |
| Storage | 50GB |
| Network Adapter | LAN Segment |
| IP Address | 192.168.100.30 |
| Role | Attack Machine |

### Ubuntu Server

The screenshot below shows the Ubuntu Server VM hardware configuration, including memory, processor allocation, and network adapter assignment to the isolated LAN Segment.

![Ubuntu Server Configuration](../images/vmware-ubuntu-network.png)

| Property | Value |
|---|---|
| Operating System | Ubuntu Server 24 |
| RAM | 4GB |
| CPUs | 2 |
| Storage | 80GB |
| Network Adapter | LAN Segment |
| IP Address | 192.168.100.10 |
| Role | SIEM Server (Wazuh) |

## VM Security Hardening

To prevent accidental data leakage between the host machine and the guest VMs, the following features were disabled on all three virtual machines.

### Shared Folders Disabled

Shared folders were disabled on all VMs to prevent files from being transferred between the host machine and the guest VMs. This ensures the isolated lab environment remains fully contained.

![Shared Folders Diabled](../images/vmware-no-shared-folders.png)

### Drag and Drop and Clipboard Disabled

Drag-and-drop and clipboard sharing were disabled on all VMs to prevent accidental copying of sensitive data between the host and guest environments. This is particularly important given that offensive security tools and intentionally vulnerable configurations are running inside the VMs.

![Clipboard Disabled](../images/vmware-no-clipboard.png)

## Baseline Snapshots

After completing the initial configuration of each VM — including OS installation, network setup, user creation, and security hardening — a baseline snapshot was taken of all three machines. A second snapshot was taken after Wazuh agent installation, Sysmon installation, and intentional vulnerability configuration on Windows 11.

These snapshots serve as clean restore points that can be used to roll back the lab environment to a known good state before running attack exercises.

| Snapshot | Description |
|---|---|
| Baseline | Taken immediately after OS installation and initial configuration |
| Pre-Exercise | Taken after full lab setup, including Wazuh agent, Sysmon, and vulnerability configuration |

## Configuration Notes

- Total RAM allocated across all three VMs is 12GB, leaving approximately 6GB of headroom on top of the host OS's normal usage of 14GB
- Storage was allocated generously on Ubuntu Server (80GB) to accommodate Wazuh log and alert data accumulation over time
- All VMs use static IP addresses, DHCP is disabled on the LAN Segment to ensure consistent addressing for Wazuh agent-to-manager communication

