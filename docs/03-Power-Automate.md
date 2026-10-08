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
```

## 3. Trigger
Action
Office 365 Outlook — When a new email arrives (V3)
Configuration
```
 Setting	                              Value
Folder	                              Inbox
From	                              OSS.Service.Assurance@sita.aero
Subject Filter	                      AAI-44: Interface SLA Report - Hourly
Only with Attachments	              Yes
Include Attachments	              No
```

The trigger starts the flow when a new email matching these criteria arrives.
The flow is event-based and does not use a recurrence trigger.

## 4. Attachment Processing
The trigger provides the list of attachments associated with the email.
An Apply to each action is used to process the attachments.
```
Email
  |
  v
Attachments
  |
  v
Apply to each
  |
  v
Get Attachment (V2)
```
This ensures that each attachment can be evaluated individually.

## 5. Get Attachment (V2)
Action
Office 365 Outlook — Get Attachment (V2)

Configuration
Message Id
Use the Message Id provided by the email trigger.

Attachment Id
Use the Attachment Id from the current item in the Apply to each loop.
The action retrieves the attachment metadata and content.
The output includes information such as:
- Attachment name
- Attachment content
- Inline status

## 6. Attachment Validation
A Condition action is used to ensure that only the required AAI-44 CSV attachment is processed.
The condition uses an AND relationship.
```
Is Inline = false
AND
Name contains "AAI-44"
AND
Name ends with ".csv"
```
Validation logic
Check 1 — Is Inline
The attachment must not be an inline attachment.
Expression:
```
outputs('Get_Attachment_(V2)')?['body/isInline']
```
Expected value:
```
false
```

Check 2 — File Name
The attachment name must contain:
```
AAI-44
```
Expression:
```
outputs('Get_Attachment_(V2)')?['body/name']
```

Check 3 — File Extension
The attachment name must end with:
```
.csv
```

Expression:
```
outputs('Get_Attachment_(V2)')?['body/name']
```
The three checks are combined using AND.
This prevents unrelated attachments from being saved.

## 7. Run ID
After the attachment passes validation, a Compose action generates a unique Run ID.
Compose — Run ID
```
concat(
    'AAI44-',
    formatDateTime(triggerOutputs()?['body/receivedDateTime'], 'yyyyMMdd-HHmmss')
)
```

Example:
```
AAI44-20261001-123512
```
The Run ID provides a timestamp-based identifier for the report processing event.

## 8. Report Date
A Compose action extracts the report date from the email received timestamp.
Compose — Report Date
```
formatDateTime(
    triggerOutputs()?['body/receivedDateTime'],
    'yyyy-MM-dd'
)
```

Example:
```
2026-10-01
```
## 9. File Timestamp
A separate timestamp is generated for the input file name.
Compose — File Timestamp
```
formatDateTime(
    triggerOutputs()?['body/receivedDateTime'],
    'yyyyMMdd_HHmmss'
)
```
Example:
```
20261001_123512
```
## 10. Raw File Name
The final file name is generated using the timestamp.
Compose — Raw File Name
```
concat(
    'AAI44_',
    outputs('Compose_-_File_Timestamp'),
    '.csv'
)
```
Example:
```
AAI44_20261001_123512.csv
```
This provides a unique and predictable name for each incoming report.

## 11. OneDrive File Creation
Action
OneDrive for Business — Create file
Folder Path
```
/AI Initiatives 2026/Agentic PlayBook/AAI44Input
```
File Name
Use:
```
Compose - Raw File Name
```

File Content
Use the Content Bytes returned by:
```
Get Attachment (V2)
```
The resulting file is saved into the OneDrive Input folder.

## 12. Final Power Automate Flow
The complete flow can be represented as:
```
┌───────────────────────────────────────┐
│ When a new email arrives (V3)        │
│                                       │
│ From: OSS.Service.Assurance@sita.aero │
│ Subject: AAI-44 : Interface SLA       │
│           Report - Hourly              │
└───────────────────┬───────────────────┘
                    │
                    ▼
          ┌───────────────────┐
          │ Apply to each     │
          │ attachment        │
          └─────────┬─────────┘
                    │
                    ▼
          ┌───────────────────┐
          │ Get Attachment    │
          │ (V2)              │
          └─────────┬─────────┘
                    │
                    ▼
          ┌───────────────────┐
          │ Validate          │
          │ attachment        │
          │                   │
          │ Is Inline = false │
          │ Name contains     │
          │ AAI-44            │
          │ Name ends .csv    │
          └─────────┬─────────┘
                    │
                 Valid
                    │
                    ▼
          ┌───────────────────┐
          │ Generate          │
          │ timestamps /      │
          │ filename          │
          └─────────┬─────────┘
                    │
                    ▼
          ┌───────────────────┐
          │ OneDrive          │
          │ Create file       │
          └─────────┬─────────┘
                    │
                    ▼
             AAI44Input
```

## 13. Responsibilities of Power Automate
Power Automate is responsible for:
- Detecting the incoming report email.
- Identifying the expected sender.
- Identifying the expected subject.
- Retrieving the attachment.
- Filtering out inline attachments.
- Validating the AAI-44 CSV.
- Creating a unique file name.
- Saving the CSV to OneDrive.
Power Automate is not responsible for:
- Parsing the CSV.
- Identifying airports.
- Transforming utilization data.
- Creating the Excel output.
- Moving files to the Processed folder.
Those responsibilities belong to the Python automation.

## 14. Dependency on Email Timing
The report is expected to arrive around the daily reporting window.
The Power Automate flow must be enabled when the email arrives.
Because the trigger is based on a new incoming email, an email that was already received before the flow was enabled will not automatically trigger the flow.

## 15. Cloud-to-Local Handoff
Once Power Automate creates the CSV in OneDrive:
```
Power Automate
      |
      v
OneDrive Cloud
      |
      | Synchronization
      v
Local AAI44Input
```
The local copy then becomes available to Windows Task Scheduler and Python.
This completes the cloud ingestion portion of the solution.

Docs folder should now look like:
```
docs/
├── 01-Solution-Overview.md
├── 02-Architecture.md
└── 03-Power-Automate.md
```
