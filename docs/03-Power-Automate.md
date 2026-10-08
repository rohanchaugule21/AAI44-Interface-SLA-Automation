# AAI-44 Interface SLA Automation — Power Automate

## 1. Purpose

Microsoft Power Automate is used to automatically detect the daily AAI-44 Interface SLA Report email and save the required CSV attachment to OneDrive.

The Power Automate flow handles only the email and file ingestion portion of the automation.

The Python transformation is handled separately by the local Windows automation.

---

## 2. Flow Overview

The Power Automate workflow is:

```text
Incoming AAI-44 Email
        |
        v
When a new email arrives (V3)
        |
        v
Apply to each attachment
        |
        v
Get Attachment (V2)
        |
        v
Validate attachment
        |
        +---- Is Inline = false
        |
        +---- Name contains "AAI-44"
        |
        +---- Name ends with ".csv"
        |
        v
Create timestamped file name
        |
        v
OneDrive - Create file
        |
        v
AAI44Input