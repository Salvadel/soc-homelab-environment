# Setup

This folder contains step-by-step installation and configuration guides for every component introduced by the AWS Cloud Integration project. Each document is scoped to a single component so it stays focused and reusable if that component is ever redeployed on its own. Rationale for why each technology and design decision was chosen is documented separately in the [Architecture Overview](../architecture/aws-cloud-integration-architecture-overview.md); these guides cover the "how," not the "why."

## Recommended Install Order

Some components depend on others being in place first; follow this order when building this project from scratch:

1. [AWS EC2 Setup](aws-ec2-setup.md) - Creates the IAM group and user, launches the EC2 instance, and locks down its security group. This must be done first, since the instance itself has to exist before a tunnel or agent can be configured on it.
2. [WireGuard Tunnel Setup](wireguard-tunnel-setup.md) - Configures the WireGuard tunnel on both pfSense and the EC2 instance, along with the firewall rules that allow tunnel traffic to reach the SIEM subnet. Requires the EC2 instance from step 1 to already be running, since the tunnel's EC2 side is configured on that instance.
3. [Wazuh Agent Setup](wazuh-agent-setup.md) - Installs and registers the Wazuh agent on the EC2 instance, pointed at the home Wazuh manager. Requires the tunnel from step 2 to be up first, since the agent cannot reach the manager without it.

## Component Purpose Summary

| Document | Component | Purpose in the Project |
|---|---|---|
| aws-ec2-setup.md | AWS IAM and EC2 | Cloud account access and the EC2 instance that serves as the cloud target |
| wireguard-tunnel-setup.md | WireGuard | Encrypted site to site tunnel connecting EC2 to the home network |
| wazuh-agent-setup.md | Wazuh Agent | Forwards EC2 telemetry to the home Wazuh manager over the tunnel |

## Other Notes

- This project assumes the core lab (pfSense, the Wazuh SIEM, and Kali Linux) is already fully built and operational; see the core lab's own documentation for that setup
- EC2's public IP is dynamic and changes when the instance is stopped and started; see the Configuration Notes in [AWS EC2 Setup](aws-ec2-setup.md) and [WireGuard Tunnel Setup](wireguard-tunnel-setup.md) for what needs updating when this happens
- Several documents reference each other directly (for example, WireGuard Tunnel Setup links back to Wazuh Agent Setup); follow those links if a step assumes something covered in another file
