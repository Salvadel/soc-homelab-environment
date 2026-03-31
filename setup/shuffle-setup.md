# Shuffle Setup

This document covers the installation and configuration of Shuffle on Ubuntu Server - SOAR. Shuffle is an open source SOAR platform used to automate alert response workflows. It receives alerts from Wazuh via webhook, enriches them with IOC data from VirusTotal and AbuseIPDB, creates cases in TheHive, and sends Slack notifications to the analyst.

## Why Shuffle

Shuffle was chosen as the SOAR platform for this lab for the following reasons:

**Open Source** - Shuffle is completely free and open source with no licensing restrictions, making it suitable for homelab use without cost.

**Visual Workflow Builder** - Shuffle provides a drag-and-drop workflow builder that makes it straightforward to build and understand automation logic without writing code.

**Native Integrations** - Shuffle has built-in integrations for Wazuh, TheHive, VirusTotal, AbuseIPDB, and Slack, covering every tool in this lab's pipeline without requiring custom development.

**Real World Relevance** - Shuffle is used in real SOC environments and demonstrates practical SOAR skills directly applicable to SOC analyst and engineer roles.

## Prerequisites

Before installing Shuffle, ensure Ubuntu Server - SOAR is fully installed, Docker is installed and running, and the static IP is configured. Full details are documented in [Ubuntu Server - SOAR Setup](soar-server-setup.md). Internet access through [pfSense](pfsense-setup.md) is required to pull the Shuffle Docker images during installation.

## Installation

Shuffle was installed on Ubuntu Server - SOAR by cloning the official Shuffle repository and starting the containers using Docker Compose. The official Shuffle repository can be found at [https://github.com/Shuffle/Shuffle](https://github.com/Shuffle/Shuffle).

**Step 1 - Clone the Shuffle repository:**
```bash
git clone https://github.com/Shuffle/Shuffle
cd Shuffle
```

**Step 2 - Start Shuffle using Docker Compose:**
```bash
docker compose up -d
```

This pulls all required Docker images and starts the Shuffle containers. The initial pull may take several minutes, depending on the internet speed.

**Step 3 - Verify Shuffle containers are running:**
```bash
docker ps
```

You should see several Shuffle containers all showing `Up` status.

![Shuffle Containers Running](../images/shuffle-container-running.png)

## Docker Configuration

After initial startup, several environment variables in `docker-compose.yml` required changes to allow Shuffle to execute workflow nodes correctly. The default configuration is designed for multi-node Docker Swarm deployments and does not work correctly on a single-node lab setup without adjustment.

Navigate to the Shuffle directory and open the compose file:
```bash
cd ~/Shuffle
nano docker-compose.yml
```

The following changes were made to the `orborus` service environment section:

**Disable Swarm mode** - The default `SHUFFLE_SWARM_CONFIG=run` causes Orborus to attempt deploying workers as Docker Swarm services, which fails on a single-node setup. Set it to `off` to use standard Docker containers instead:
```yaml
- SHUFFLE_SWARM_CONFIG=off
```

**Set the worker server URL** - `SHUFFLE_WORKER_SERVER_URL` was empty by default, causing Orborus to fall back to an unresolvable hostname. Set it to the SOAR server's LAN IP:
```yaml
- SHUFFLE_WORKER_SERVER_URL=http://192.168.100.40:33333
```

**Set the correct backend URL** - `BASE_URL` must point to the backend container using its internal Docker hostname and backend port, not the frontend port:
```yaml
- BASE_URL=http://shuffle-backend:5001
```

After making these changes, restart the containers:
```bash
docker compose down
docker compose up -d
```

Verify Orborus is connecting to the backend correctly:
```bash
docker logs shuffle-orborus --tail 20
```

The log should show `Got statuscode 200 from backend on first request` and `New Worker created` entries, indicating the execution engine is functioning.

## Accessing the Dashboard

The Shuffle dashboard is accessible from the Windows 11 VM browser at:
```
http://192.168.100.40:3001
```

On first access, Shuffle will prompt you to create an admin account. The following credentials were used:

| Field | Value |
|---|---|
| Email | admin@soc.local |
| Password | set during installation |

![Shuffle Dashboard](../images/shuffle-dashboard.png)

## Wazuh Integration

Wazuh is configured to forward alerts to Shuffle via a webhook trigger. When a qualifying alert fires in Wazuh, it sends the alert data to Shuffle, which begins the automation workflow.

### Step 1 - Create a Webhook Trigger in Shuffle

- In the Shuffle dashboard, navigate to **Workflows**
- Click **Create Workflow** and name it `Wazuh Alert Pipeline`
- In the workflow editor, drag a **Webhook** trigger onto the canvas
- Click the webhook trigger and copy the generated webhook URL - it will look like:
```
http://192.168.100.40:3001/api/v1/hooks/webhook_XXXXXXXX
```

### Step 2 - Configure Wazuh to Forward Alerts

On Ubuntu Server - SIEM, edit the Wazuh Manager configuration file:
```bash
sudo nano /var/ossec/etc/ossec.conf
```

Add the following integration block before the closing `</ossec_config>` tag:
```xml
<integration>
  <name>shuffle</name>
  <hook_url>http://192.168.100.40:3001/api/v1/hooks/webhook_XXXXXXXX</hook_url>
  <level>7</level>
  <alert_format>json</alert_format>
</integration>
```

Replace `webhook_XXXXXXXX` with your actual webhook URL copied from Shuffle. The `<level>7</level>` setting means only alerts of severity level 7 and above are forwarded to Shuffle.

Restart the Wazuh Manager to apply the change:
```bash
sudo systemctl restart wazuh-manager
```

![Wazuh Integration Block](../images/shuffle-wazuh-integration.png)

## IOC Enrichment

Shuffle is configured to automatically enrich incoming Wazuh alerts with threat intelligence data by querying VirusTotal and AbuseIPDB for the source IP address extracted from each alert. Both enrichment nodes run in parallel immediately after the webhook trigger.

### VirusTotal Integration

A free VirusTotal API key is required. Register at [https://www.virustotal.com](https://www.virustotal.com) to obtain a free API key.

In the Shuffle workflow editor:
- Add a **VirusTotal** app action connected directly to the webhook trigger
- Select the **Get IP Report** action
- Enter your VirusTotal API key in the authentication field
- Set the IP field to the source IP extracted from the Wazuh alert

### AbuseIPDB Integration

A free AbuseIPDB API key is required. Register at [https://www.abuseipdb.com](https://www.abuseipdb.com) to obtain a free API key.

In the Shuffle workflow editor:
- Add an **AbuseIPDB** app action connected directly to the webhook trigger, parallel to the VirusTotal node
- Select the **Check IP** action
- Enter your AbuseIPDB API key in the authentication field
- Set the IP field to the same source IP variable used for VirusTotal

## TheHive Integration

Shuffle creates an alert in TheHive for each qualifying Wazuh alert using an HTTP node pointed directly at the TheHive API. The native Shuffle TheHive app was not used due to a variable resolution bug in the installed version that caused `$exec.*` variables to be sent as literal strings instead of resolved values.

In the Shuffle workflow editor, add an **HTTP** app action connected after both the VirusTotal and AbuseIPDB nodes and configure it as follows:

**Method:** `POST`

**URL:**
```
http://172.17.0.1:9000/api/v1/alert
```

The IP `172.17.0.1` is the Docker bridge gateway address, which is how containers reach services running on the host machine. Using the LAN IP `192.168.100.40` does not work from inside Docker containers.

**Headers:**
```
Authorization: Bearer YOUR_THEHIVE_API_KEY
Content-Type: application/json
```

Use the API key generated for the `shuffle@soc.local` user in TheHive. Full details on the API key are documented in [TheHive Setup](thehive-setup.md).

**Body:**
```json
{
  "title": "$exec.title",
  "description": "$exec.title",
  "severity": $exec.severity,
  "type": "internal",
  "source": "Wazuh",
  "sourceRef": "$exec.id",
  "tags": ["wazuh", "automated"]
}
```

Note that `$exec.severity` has no quotes because TheHive expects an integer, not a string.

## Slack Integration

Shuffle sends a Slack notification after the TheHive alert is created using an HTTP node pointed at the Slack incoming webhook URL.

### Step 1 - Create a Slack Workspace and Webhook

- Go to [https://slack.com](https://slack.com) and create a free workspace
- Create a channel named `#soc-alerts`
- Go to **Apps > Incoming Webhooks** and create a new webhook for the `#soc-alerts` channel
- Copy the webhook URL - it will look like:
```
https://hooks.slack.com/services/XXXXXXXX/XXXXXXXX/XXXXXXXX
```

### Step 2 - Add Slack HTTP Node to Workflow

In the Shuffle workflow editor, add an **HTTP** app action connected after the TheHive node and configure it as follows:

**Method:** `POST`

**URL:** Your Slack webhook URL

**Body:**
```json
{"text": "Wazuh Alert | Rule ID: $exec.rule_id | Severity: $exec.severity | Agent: $exec.all_fields.agent.name | TheHive ID: $http_1.body._id"}
```

The body uses pipe separators instead of newlines to avoid JSON parsing errors caused by special characters in alert titles. `$http_1.body._id` references the TheHive alert ID returned by the previous HTTP node, providing a direct reference to the created alert.

![Slack Alert Received](../images/slack-alert-recieved.png)

## Complete Workflow

The completed Shuffle workflow connects all five steps into a single automated pipeline. 

```
Wazuh Alert
    |
Webhook Trigger
    |
VirusTotal         
    |
AbuseIPDB
    |
TheHive Alert Created
    |
Slack Notification Sent
```

![Shuffle Execution Success](../images/shuffle-execution-success.png)

## Troubleshooting Encountered

### Shuffle Dashboard Not Loading

After starting the containers with `docker compose up -d` the Shuffle dashboard returned a connection refused error when accessed from the Windows 11 browser.

**Root cause:** Shuffle containers take several minutes to fully initialize after starting. The dashboard is not immediately available even when `docker ps` shows all containers as running.

**Resolution:** Waiting 3-5 minutes after container startup and retrying the browser resolved the issue.

### Workflow Nodes Hanging on Execution

Workflow nodes, including basic echo tests, would hang indefinitely with no result.

**Root cause:** Three misconfigured environment variables in `docker-compose.yml` prevented Orborus from spawning and communicating with worker containers. `SHUFFLE_SWARM_CONFIG=run` caused Orborus to attempt Docker Swarm service deployments which fails on a single-node setup. `SHUFFLE_WORKER_SERVER_URL` was empty, causing Orborus to fall back to an unresolvable hostname. `BASE_URL` pointed to the frontend port 3001 instead of the backend port 5001.

**Resolution:** Set `SHUFFLE_SWARM_CONFIG=off`, `SHUFFLE_WORKER_SERVER_URL=http://192.168.100.40:33333`, and `BASE_URL=http://shuffle-backend:5001` in the orborus service environment section of `docker-compose.yml`, then restarted the containers.

### TheHive Alerts Returning 400 Invalid JSON

The native Shuffle TheHive app returned a 400 Bad Request error with an `Unrecognized token '$'` message.

**Root cause:** A variable resolution bug in the installed version of the Shuffle TheHive app caused `$exec.*` variables to be sent as literal strings instead of resolved values.

**Resolution:** Replaced the native TheHive app with an HTTP node configured to POST directly to `http://172.17.0.1:9000/api/v1/alert`. The HTTP node resolves Shuffle variables correctly before sending the request.

### Slack Notifications Returning SyntaxError

The Slack HTTP node returned a `SyntaxError - unterminated string literal` when alert titles were interpolated into the message body.

**Root cause:** Wazuh rule descriptions, such as CIS benchmark titles, contain apostrophes and quotes that break JSON string parsing when used directly in the message body.

**Resolution:** Replaced `$exec.title` in the Slack body with fields that only contain safe characters - `$exec.rule_id`, `$exec.severity`, `$exec.all_fields.agent.name`, and `$http_1.body._id`.

## Configuration Notes

- Shuffle runs via Docker Compose and starts automatically on boot
- The Shuffle dashboard is accessible at `http://192.168.100.40:3001`
- Docker Compose configuration is located at `~/Shuffle/docker-compose.yml`
- The Wazuh integration forwards alerts of severity level 7 and above to Shuffle
- TheHive is reached from inside Shuffle using the Docker bridge gateway `172.17.0.1` rather than the LAN IP
- VirusTotal free tier allows 4 API lookups per minute, which is sufficient for homelab usage
- AbuseIPDB free tier allows 1000 lookups per day, which is sufficient for homelab usage
- The complete workflow connects Wazuh, VirusTotal, AbuseIPDB, TheHive, and Slack in a single automated pipeline
- Full Shuffle documentation is available at [https://shuffler.io/docs](https://shuffler.io/docs)
