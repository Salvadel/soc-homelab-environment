# Ubuntu Server - SOAR Setup

This document covers the installation and configuration of the Ubuntu Server - SOAR virtual machine in the SOC homelab. Ubuntu Server - SOAR serves as the SOAR host, running Shuffle for automated response workflows and TheHive for case management. Full installation details for each tool are documented separately in [Shuffle Setup](shuffle-setup.md) and [TheHive Setup](thehive-setup.md).

## VM Specifications

| Property | Value |
|---|---|
| Operating System | Ubuntu Server 24 |
| RAM | 20GB |
| CPUs | 4 |
| Storage | 80GB |
| Network Adapter | LAN Segment |
| IP Address | 192.168.100.40 |
| Gateway | 192.168.100.1 (pfSense) |
| Role | SOAR Server (Shuffle / TheHive) |

## Installation

Ubuntu Server - SOAR was installed as a virtual machine in VMware Workstation using the official Ubuntu Server ISO. During installation, the static IP, gateway, and DNS were configured directly through the installer network configuration screen. No desktop environment was installed - Ubuntu Server runs headless via terminal only, which reduces resource usage. The official Ubuntu Server ISO can be downloaded from the [Ubuntu official download page](https://ubuntu.com/download/server).

Storage was allocated at 80GB to accommodate TheHive case data and Docker container storage accumulation over time as lab exercises are performed.

### Ubuntu Server - SOAR Terminal

The screenshot below confirms the Ubuntu Server - SOAR VM is fully installed and operational.

![Ubuntu Server SOAR Terminal](../images/soar-terminal.png)

## Network Configuration

A static IP address was assigned to the Ubuntu Server - SOAR VM during installation to ensure consistent addressing within the LAN Segment. The default gateway is set to 192.168.100.1, pointing to [pfSense](pfsense-setup.md). All internet-bound traffic from this machine routes through pfSense via VMware NAT, which is required for Docker installation, Slack notification delivery, and IOC enrichment queries to VirusTotal and AbuseIPDB. Internal traffic to other VMs stays on the LAN Segment and bypasses pfSense entirely.

### Static IP Assignment

| Property | Value |
|---|---|
| IP Address | 192.168.100.40 |
| Subnet Mask | 255.255.255.0 |
| Gateway | 192.168.100.1 |
| DNS | 192.168.100.1 (pfSense) |

The following configuration was applied during installation:

| Field | Value |
|---|---|
| Subnet | 192.168.100.0/24 |
| Address | 192.168.100.40 |
| Gateway | 192.168.100.1 |
| Name servers | 192.168.100.1 |
| Search domains | leave blank |

The screenshot below shows the output of the command `ip a`, confirming the static IP address is active on the Ubuntu Server - SOAR VM.

![SOAR IP Configuration](../images/soar-ip-config.png)

The screenshot below shows the output of the command `ip route`, confirming the default gateway is correctly set to 192.168.100.1.

![SOAR IP Route](../images/soar-ip-route.png)

## System Update

After installation, the system package list and all installed packages were updated to ensure the latest libraries and security patches are in place before tool installation.
```bash
sudo apt update && sudo apt upgrade -y
```

## Docker Installation

Docker is required to run Shuffle and TheHive. Docker was installed on Ubuntu Server - SOAR using the official Docker installation method for Ubuntu. The official Docker installation guide for Ubuntu can be found at the [Docker Engine Installation Guide](https://docs.docker.com/engine/install/ubuntu/).

Install Docker dependencies:
```bash
sudo apt install ca-certificates curl gnupg -y
```

Add Docker's official GPG key:
```bash
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg
```

Add the Docker repository:
```bash
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```

Install Docker:
```bash
sudo apt update
sudo apt install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin -y
```

Verify Docker is running:
```bash
sudo systemctl status docker
```

Expected output should show **active (running)**.

![Docker Running](../images/soar-docker-running.png)

## SOAR Services

Shuffle and TheHive are installed and running on Ubuntu Server - SOAR. Both services are configured to start automatically on boot via Docker. Shuffle is configured to enrich incoming Wazuh alerts with IOC data from VirusTotal and AbuseIPDB before creating cases in TheHive and sending Slack notifications to the analyst. Full installation details are documented in [Shuffle Setup](shuffle-setup.md) and [TheHive Setup](thehive-setup.md). The official TheHive Docker installation guide can be found at the [TheHive Docker Deployment Guide](https://docs.strangebee.com/thehive/installation/docker/).

To verify both services are running:
```bash
sudo docker ps
```

The screenshot below confirms all SOAR services are active and running.

![SOAR Services Running](../images/soar-services-running.png)

## Connectivity Verification

After static IP assignment, connectivity was verified across the most critical communication path for Ubuntu Server - SOAR. For full network connectivity verification across all critical lab communication paths, see [Static IP Configuration](../architecture/static-ip-configuration.md).

### Ubuntu Server - SOAR → pfSense Gateway
Confirms the SOAR server can reach the gateway. If this fails, Slack notifications cannot be sent.
```bash
ping 192.168.100.1
```

![Ping Test SOAR to Gateway](../images/ping-test-soar-to-gateway.png)

## Configuration Notes

- Ubuntu Server - SOAR runs headless with no desktop environment installed, reducing RAM and CPU overhead and leaving more resources available for the SOAR stack
- 20GB RAM was allocated to accommodate the memory requirements of both Shuffle and TheHive running simultaneously
- 80GB storage was allocated to accommodate TheHive case data and Docker container storage accumulation over time
- All SOAR services start automatically on boot via Docker, meaning the SOAR stack is fully operational as soon as the VM boots without manual intervention
- The Shuffle dashboard is accessible via browser from the Windows 11 VM at `http://192.168.100.40:3001`
- The TheHive dashboard is accessible via browser from the Windows 11 VM at `http://192.168.100.40:9000`
- Internet access is available through [pfSense](pfsense-setup.md) via VMware NAT for Docker installation, tool downloads, Slack notification delivery, and IOC enrichment queries to VirusTotal and AbuseIPDB
- Username on this VM is `soarsadmin`
