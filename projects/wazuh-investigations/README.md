# Wazuh Investigations

A series of Kali attack simulations against a Windows 11 lab host, investigated in Wazuh SIEM, documented, and mapped to MITRE ATT&CK techniques.

Each investigation lives in its own folder and includes:

- The attack script itself
- A README containing the full investigation write-up, findings, and screenshots

## Setup

This section explains the general process for setting up and running any investigation script in this series. Every investigation folder follows this same pattern, with investigation-specific details (credentials, target accounts, unique flags) documented in that investigation's own README instead of here.

### Prerequisites

The [core lab](https://github.com/Salvadel/soc-homelab-environment/blob/main/core-lab/README.md) must be fully built out before running any investigation in this series.

### Steps

1. Navigate to the respective investigation folder

```
cd wazuh-investigations/<investigation-folder>
```

2. Confirm the attack script for that investigation is present in the folder

3. Run the script using Python 3 from Kali Linux
python3 /path-to-file

```
```

Example

```
python3 password_spray.py
```

4. Let the script run to completion. Do not interrupt it partway through; an incomplete run can leave a misleading dataset

5. Confirm the Wazuh agent is picking up the generated events under the relevant event channel on the Windows target

6. Check the investigation's README for the specific event IDs, expected event count, and any script-specific flags before starting the analysis

***Note: the script can take a long time to run depending on the resources allocated and the speed of your machine, may take multiple hours***

## Investigations

| # | Investigation | # of Logs | MITRE Technique | Status |
|---|---|---|---|---|
| 01 | [Password Spraying](./password-spraying/) | ~4,750 | T1110 & T1110.003, Brute Force: Password Spraying | Completed |
| 02 | [Living off the Land](./living-off-the-land/) | ~1,000 | T1546.001, Event Triggered Execution: Application Shimming | Completed |

***More investigations will be added here as they are completed. The plan is for around 10 total, covering different attack techniques and detection scenarios.***
