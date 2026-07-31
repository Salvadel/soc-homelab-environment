# Projects

This folder holds every project that expands on the core lab. Each project lives in its own folder with its own `README.md`, `architecture/`, `setup/`, and `images/`, and documents a self-contained addition to the lab built on top of the core infrastructure.

## Project Index

| Project | Status | Overview |
|---|---|---|
| [SOAR Automation](soar-automation/README.md) | In Progress | Adds security orchestration and automated response on top of the core lab. Automates the SOC analyst's response to Wazuh alerts by enriching them with threat intelligence, creating a case in TheHive, and sending a Slack notification, using Shuffle. |
| AWS Wazuh Log Ingestion | In Progress | Documentation not yet started. |

## Adding a New Project

Each project should follow this structure:

```
projects/<project-name>/
├── README.md
├── execution.md (validates project workflow and objectives)
├── architecture/
│   ├── README.md
│   └── <project-name>-architecture-overview.md
├── setup/
│   ├── README.md
│   └── (one setup document per component)
└── images/
    └── (screenshots and diagrams referenced throughout the project's documentation)
```

**Note: Every project assumes the [Core Lab](../core-lab/README.md) is already fully built and operational, and should state any additional prerequisites specific to that project in its own README.**
