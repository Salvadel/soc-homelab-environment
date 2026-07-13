# TheHive Setup

This document covers the installation and configuration of TheHive on the Ubuntu Server SOAR host. TheHive is an open-source security incident response platform used for case management and investigation. It receives cases automatically from Shuffle when Wazuh generates alerts and provides a structured workflow for the SOC analyst to investigate and respond to incidents.

## Prerequisites

Before installing TheHive, ensure the Ubuntu Server SOAR host is fully installed, the static IP is configured, and system packages have been updated. Full details are documented in [Ubuntu Server Setup (SOAR)](ubuntu-soar-setup.md). Internet access through pfSense is required to download the TheHive installation script.

## TheHive Stack Components

TheHive relies on three components, all installed on the Ubuntu Server SOAR host:

| Component | Description |
|---|---|
| Cassandra | NoSQL database used by TheHive to store case and alert data |
| Elasticsearch | Search and indexing engine used by TheHive for data retrieval |
| TheHive | Web-based case management platform and investigation interface |

## Installation

TheHive was installed using the official StrangeBee installation script, which automates the deployment of all three stack components. The official installation guide can be found at [TheHive Installation Guide](https://docs.strangebee.com/thehive/installation/).

Run the following command on the Ubuntu Server SOAR host:
```bash
wget -q -O /tmp/install_script.sh https://scripts.download.strangebee.com/latest/sh/install_script.sh ; sudo -v ; bash /tmp/install_script.sh
```

When prompted, select option **2 - Install TheHive**. The script handles all dependency installation, service configuration, and initial setup automatically.

## Enabling Services on Boot

After installation, all three services were enabled to start automatically on boot:
```bash
sudo systemctl enable cassandra
sudo systemctl enable elasticsearch
sudo systemctl enable thehive
```

Verify all three are enabled:
```bash
sudo systemctl is-enabled cassandra
sudo systemctl is-enabled elasticsearch
sudo systemctl is-enabled thehive
```

All three should return `enabled`.

## Verifying Services

After installation, all three services were verified as active and running:
```bash
sudo systemctl status cassandra
sudo systemctl status elasticsearch
sudo systemctl status thehive
```

![TheHive Services Running](../images/thehive-services-running.png)

## Accessing the Dashboard

The TheHive dashboard is accessible from the Windows 11 VM browser at:
```
http://192.168.40.40:9000
```

Default credentials on first login:
- Username: `admin`
- Password: `secret`

The default password was changed immediately after the first login.

![TheHive Dashboard](../images/thehive-dashboard.png)

## Initial Configuration

### License Registration

TheHive installs with a 16 day Platinum trial license. A free Community license was requested from StrangeBee to replace the trial before expiry. The Community license can be requested at [StrangeBee Community Edition](https://docs.strangebee.com/thehive/installation/licenses/request-a-community-license).

Once the license key is received, apply it by navigating to:
```
Admin > License > Enter License Key
```

### Organisation Setup

A dedicated organisation was created for the lab:

- Go to **Admin > Organisations > Create Organisation**
- Name: `SOC-Homelab`
- Task sharing rule: `Manual`
- Observables sharing rule: `Manual`

![TheHive Organization](../images/thehive-organization.png)

### Shuffle Integration User

A dedicated service account was created for Shuffle to use when creating cases automatically:

| Field | Value |
|---|---|
| Login | shuffle@soc.local |
| Name | Shuffle Integration |
| Profile | analyst |
| Organisation | SOC-Homelab |

An API key was generated for the admin account for direct API access and saved separately.

![TheHive Admin API Key](../images/thehive-api-key.png)

A second API key was generated specifically for the `shuffle@soc.local` integration user, this is the key referenced in [Shuffle Setup](shuffle-setup.md) for the TheHive HTTP integration node.

![TheHive Shuffle User API Key](../images/thehive-soclab-api-key.png)

## Starting TheHive After Reboot

TheHive services start automatically on boot. If manual startup is required, start the services in this exact order and wait between each:
```bash
sudo systemctl start cassandra
```

Wait 5 minutes, then:
```bash
sudo systemctl start elasticsearch
```

Wait 2 minutes, then:
```bash
sudo systemctl start thehive
```

TheHive will be accessible at `http://192.168.40.40:9000` within a few minutes of the service starting.

## Troubleshooting Encountered

### TheHive Failing on Startup with Exit Code

After initial installation, TheHive repeatedly failed to start with a `failed with result exit-code` error.

**Root cause:** TheHive was attempting to connect to Cassandra before Cassandra had fully initialized its keyspaces and was ready to accept connections.

**Resolution:** Starting Cassandra first and waiting 5 minutes before starting TheHive resolved the issue. The services were then enabled to start automatically on boot in the correct order using `systemctl enable`.

## Configuration Notes

- TheHive, Cassandra, and Elasticsearch are all set to start automatically on boot via `systemctl enable`
- TheHive uses a free Community license from StrangeBee; the license must be applied within 16 days of installation to prevent the instance from entering read-only mode
- The default admin password was changed immediately after the first login
- Cassandra is the slowest service to initialize; always wait at least 5 minutes after Cassandra starts before attempting to access the TheHive dashboard
- Task sharing and observable sharing rules are set to Manual to mirror real SOC data handling practices
- Full TheHive documentation is available at [https://docs.strangebee.com](https://docs.strangebee.com)
