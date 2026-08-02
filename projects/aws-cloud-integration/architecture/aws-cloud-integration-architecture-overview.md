# Architecture Overview

This document explains the design decisions behind the AWS Cloud Integration project: why each technology was chosen, how the network is structured and addressed, and how all components communicate with each other. Step-by-step installation and configuration for each component is documented separately in the [setup](../setup/) folder.

## Network Diagram

![AWS Cloud Integration Network Architecture](../images/aws-integration-network-architecture-diagram.png)

This project extends the core SOC homelab with a hybrid on-prem/cloud monitoring capability. An AWS EC2 instance is deployed as a cloud target, connected back to the home network over a WireGuard VPN tunnel through pfSense, and monitored by the existing home Wazuh manager. An attack is simulated against the EC2 instance from Kali Linux to validate that the home SIEM can detect activity on a cloud hosted endpoint the same way it detects activity on-prem.

| Device | Role | Location | Subnet | Address | Gateway / Peer |
|---|---|---|---|---|---|
| pfSense (WG_AWS interface) | WireGuard tunnel server endpoint | Home (VMware), new tunnel interface | 10.10.10.0/24 | 10.10.10.1 | N/A |
| EC2 Instance | Cloud target, Wazuh agent (AWS_Ubuntu) | AWS, t3.micro | 10.10.10.0/24 (tunnel) | 10.10.10.2 | 10.10.10.1 |
| Wazuh Manager | SIEM, receives logs from all agents including EC2 | Home (VMware), SOC-Lab-SIEM | 192.168.10.0/24 | 192.168.10.10 | 192.168.10.1 |
| Kali Linux | Attack simulation source | Home (VMware), SOC-Lab-Kali | 192.168.30.0/24 | 192.168.30.30 | 192.168.30.1 |

## Why WireGuard Over a Direct Port Forward

WireGuard was chosen as the connection method between AWS and the home network for the following reasons:

**Encryption and Authentication** - The simplest way to get EC2 logs into the home Wazuh manager would have been to open the Wazuh manager's port directly to the internet and point the EC2 agent at the home public IP. A WireGuard tunnel was chosen instead because it gives the connection its own encrypted, authenticated channel rather than relying on an open, unauthenticated path across the internet.

**Reduced Exposure** - Routing agent traffic through the tunnel keeps the Wazuh manager itself unreachable from the open internet, exposing only the WireGuard port rather than the SIEM's own listening port.

**Enterprise Relevance** - Bridging an on-prem SIEM to a cloud workload over a VPN tunnel reflects how a real hybrid enterprise environment, and a SOC or cloud engineer, would actually design this kind of connection.

## Why pfSense as the WireGuard Server

pfSense was chosen as the tunnel endpoint for the following reasons:

**Existing Central Role** - pfSense was already the central router and firewall for the entire home lab, so it made sense for it to also be the tunnel endpoint rather than introducing a second device or terminating the tunnel directly on the Wazuh manager.

**Consistent Design Pattern** - This keeps pfSense as the single point that controls what traffic is allowed to move between network segments, including the new segment this project introduces, matching how the core lab is already structured.

## Why a Separate Tunnel Subnet (10.10.10.0/24)

The WireGuard tunnel uses its own subnet, 10.10.10.0/24, rather than extending one of the existing 192.168.x.0/24 lab subnets, for the following reason:

**Addressing Clarity** - Anyone reading the architecture can immediately tell that 10.10.10.0/24 is the cloud bridge, not another on-prem LAN segment, without needing to cross-reference a table. pfSense holds 10.10.10.1 and the EC2 instance holds 10.10.10.2.

## Why the EC2 Instance Initiates the Tunnel

The EC2 peer on pfSense is configured with a dynamic endpoint rather than a fixed one, for the following reasons:

**No Static Public IP Required** - EC2 does not have a stable IP from pfSense's point of view unless an Elastic IP is allocated, and this project intentionally avoided that to stay within free tier usage.

**EC2 Maintains the Connection** - EC2 initiates the WireGuard handshake outward toward pfSense's public IP, and a PersistentKeepalive value keeps that connection alive from the EC2 side, so pfSense always has a live path back regardless of EC2's current IP.

## Why AmazonEC2FullAccess Instead of AdministratorAccess

The IAM user created for this project, soc-lab-admin, was granted AmazonEC2FullAccess through an IAM group rather than AdministratorAccess, for the following reasons:

**Least Privilege** - This project's scope only requires launching, managing, and terminating EC2 resources, so broader account-level access was unnecessary and would have increased the blast radius if these credentials were ever exposed.

**Group-Based Permissions** - Permissions were attached to a group, soc-lab-admins, rather than directly to the user, so future users or automation accounts can be added without re-attaching policies.

## Why the Security Group Is Restricted to a Single IP

The EC2 instance's security group allows inbound SSH only from the operator's home IP address, rather than 0.0.0.0/0, for the following reason:

**Minimal Attack Surface** - The WireGuard tunnel handles all SIEM-related traffic on its own encrypted channel, so the only reason SSH needs to be reachable at all is for direct administration, and there is no reason for that to be open to the whole internet.

## Why Traffic Reaching the SIEM Subnet Requires Two Firewall Rules

Reaching the Wazuh manager from EC2 requires a rule on the tunnel interface (CLOUDUBUNTU) and a separate rule on the SIEM interface (WAZUH), for the following reason:

**Per-Interface Rule Evaluation** - pfSense evaluates firewall rules per interface, for traffic entering that interface. The SIEM interface's default rules only permit traffic sourced from its own local subnet outbound, so a rule allowing traffic to arrive from the tunnel subnet is needed in addition to the rule allowing traffic to leave the tunnel interface. Both rules were scoped to the specific source and destination needed, the EC2 tunnel address and the Wazuh manager's IP on TCP 1514, rather than left open, consistent with the least-privilege approach used elsewhere in this project.

## Relationship to the Core Lab

This project's pfSense configuration builds on top of the core lab's existing pfSense setup rather than replacing it. The core lab's own architecture and setup documentation remain a snapshot of the lab at the time they were written and are not retroactively updated here. This document, and the setup files in this project folder, are the authoritative source for anything added or changed as part of this cloud integration.
