# AAI-44 Interface SLA Automation — Architecture

## 1. Architecture Overview

The AAI-44 automation follows a hybrid cloud and local execution architecture.

The cloud portion is responsible for receiving and storing the daily report, while the local portion is responsible for executing the Python transformation.

```text
                    CLOUD
        ┌──────────────────────────┐
        │                          │
        │   Outlook / Office 365   │
        │            │             │
        │            ▼             │
        │   Power Automate Flow    │
        │            │             │
        │            ▼             │
        │   OneDrive for Business  │
        │                          │
        └────────────┬─────────────┘
                     │
              OneDrive Sync
                     │
                     ▼
                    LOCAL
        ┌──────────────────────────┐
        │                          │
        │     Windows Machine      │
        │            │             │
        │            ▼             │
        │    Windows Task          │
        │      Scheduler           │
        │            │             │
        │            ▼             │
        │    Python Automation     │
        │            │             │
        │            ▼             │
        │   Structured Excel       │
        │                          │
        └──────────────────────────┘