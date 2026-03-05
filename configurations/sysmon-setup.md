# Sysmon Setup

This document covers the installation and configuration of Sysmon (System Monitor) on the Windows 11 target endpoint. Sysmon is a free Microsoft Sysinternals tool that significantly enhances the quality and detail of endpoint logs collected by the Wazuh agent, providing visibility into process creation, network connections, and file system activity that standard Windows Event Logs do not capture.

## Why Sysmon

The default Windows Event Logs forwarded by the Wazuh agent provide limited visibility into endpoint activity. Without Sysmon, many attack techniques leave little or no trace in standard logs. Sysmon fills this gap by generating detailed telemetry at the system level, including:

- Process creation with full command line arguments
- Parent-child process relationships
- Network connection attempts, including source and destination IPs
- File creation and modification events
- Driver and DLL loading events

This additional telemetry is essential for detecting and investigating the attack simulations conducted in this lab and reflects how Sysmon is commonly deployed alongside SIEM agents in real enterprise environments.

## Download

Sysmon is part of the Microsoft Sysinternals suite and can be downloaded directly from the [Microsoft Sysinternals official download page](https://learn.microsoft.com/en-us/sysinternals/downloads/sysmon). The zip archive contains four files:

| File | Description |
|---|---|
| Sysmon.exe | 32-bit version — not used |
| Sysmon64.exe | 64-bit version — used for this lab |
| Sysmon64a.exe | ARM 64-bit version — not used |
| Eula.txt | License agreement |

Since Windows 11 is a 64-bit operating system, **Sysmon64.exe** is the correct binary.

The Sysmon folder was saved to `C:\Tools\Sysmon\` for permanent storage. This location is important as the executable is required for future updates, configuration changes, or reinstallation.

## Installation

Sysmon was installed via PowerShell running as Administrator. Navigate to the Sysmon folder and run:
```powershell
cd C:\Tools\Sysmon
.\Sysmon64.exe -accepteula -i
```

The `-accepteula` flag silently accepts the license agreement, and `-i` initiates the installation.

### Installation Screenshot

![Sysmon Installation Output](../images/sysmon-install.png)

## Verify Sysmon is Running

After installation, confirm Sysmon is running as a service:
```powershell
Get-Service Sysmon64
```

Expected output should show **Status: Running**.

### Service Verification Screenshot

![Sysmon Service Running](../images/sysmon-service-running.png)

## Auto-Start on Boot

Sysmon was configured to start automatically on system boot, so it does not need to be manually started each session. This was configured via the Windows Services manager (`services.msc`) by setting the Sysmon64 service Startup Type to **Automatic**.

## Wazuh Integration

No additional configuration is required on the Wazuh side to begin collecting Sysmon logs once the Sysmon log channel has been added to ossec.conf. Full details on the ossec.conf configuration is documented in [Wazuh Agent Setup](wazuh-agent-setup.md).

Sysmon events appear in the Wazuh dashboard under the Windows agent's event log view and can be filtered using:
```
rule.groups: sysmon
```

### Wazuh Dashboard Showing Sysmon Events

![Sysmon Events in Wazuh Dashboard](../images/wazuh-sysmon-events.png)

## Configuration Notes

- Sysmon64.exe is stored permanently at `C:\Tools\Sysmon\` and should not be deleted
- No custom Sysmon configuration file has been applied — Sysmon is running with default settings
- A future improvement is to apply a community ruleset, such as the SwiftOnSecurity Sysmon config to further improve detection coverage and reduce noise
- Sysmon version can be checked by running `.\Sysmon64.exe` with no arguments in the installation directory
