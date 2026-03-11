# Static IP Configuration

This document outlines the static IP configuration applied to each virtual machine in the SOC homelab. Static IPs are used in place of DHCP to ensure consistent addressing across all machines, which is critical for Wazuh agent-to-manager communication, reliable attack simulation targeting, and pfSense gateway routing. For a visual overview of how these machines connect, see [Architecture Overview](architecture-overview.md).

## Network Information

| Property | Value |
|---|---|
| Network Type | VMware LAN Segment |
| Subnet | 192.168.100.0/24 |
| Subnet Mask | 255.255.255.0 |
| Gateway | 192.168.100.1 (pfSense) |
| DHCP | Disabled |
| Internet Access | Via pfSense NAT |

## IP Assignment Table

| Machine | OS | IP Address | Subnet Mask | Gateway | Role |
|---|---|---|---|---|---|
| pfSense | pfSense CE | 192.168.100.1 | 255.255.255.0 | N/A | Firewall / Router |
| Ubuntu Server - SIEM | Ubuntu Server 24 | 192.168.100.10 | 255.255.255.0 | 192.168.100.1 | SIEM Server (Wazuh) |
| Windows 11 | Windows 11 Home | 192.168.100.20 | 255.255.255.0 | 192.168.100.1 | Target Endpoint |
| Kali Linux | Kali Linux 2025.4 | 192.168.100.30 | 255.255.255.0 | 192.168.100.1 | Attack Machine |
| Ubuntu Server - SOAR | Ubuntu Server 24 | 192.168.100.40 | 255.255.255.0 | 192.168.100.1 | SOAR Server |

## Connectivity Verification

Connectivity between all machines was verified using ping after static IP assignment. All machines were confirmed able to reach the pfSense gateway and each other across the LAN Segment.

### Windows 11 → Ubuntu Server - SIEM
```
ping 192.168.100.10
```
![Ping Test Windows to Server](../images/ping-test-windows-to-server.png)

### Windows 11 → Kali Linux
```
ping 192.168.100.30
```
![Ping Test Windows to Kali](../images/ping-test-windows-to-kali.png)

### Kali Linux → Windows 11
```
ping 192.168.100.20
```
![Ping Test Kali to Windows](../images/ping-test-kali-to-windows.png)

### Kali Linux → Ubuntu Server - SIEM
```
ping 192.168.100.10
```
![Ping Test Kali to Server](../images/ping-test-kali-to-server.png)

### All Machines → pfSense Gateway
```
ping 192.168.100.1
```
![Ping Test to Gateway](../images/ping-test-gateway.png)

### Ubuntu Server - SOAR → Ubuntu Server - SIEM
```
ping 192.168.100.10
```
![Ping Test SOAR to SIEM](../images/ping-test-soar-to-siem.png)

## Configuration Notes

- All static IPs were assigned manually through each VM's network settings
- All VMs are configured with a default gateway of 192.168.100.1 pointing to pfSense
- Internet bound traffic from any VM routes through pfSense before reaching the internet via VMware NAT
- Internal VM to VM traffic stays on the LAN Segment and does not pass through pfSense
- DNS is handled by pfSense which forwards DNS queries upstream through the NAT adapter
- IP assignments were confirmed stable across VM reboots before proceeding with tool installations
