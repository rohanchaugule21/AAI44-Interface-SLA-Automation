# AAI44 Interface SLA Automation

Automated processing of the AAI-44 Interface SLA Report using Microsoft Power Automate, OneDrive for Business, Windows Task Scheduler, and Python.

---

## 1. Overview

The AAI-44 Interface SLA Report was previously processed through a manual workflow where the daily CSV report received through email had to be downloaded and processed using a Python script.

This agentic playbook solution automates the complete workflow from receiving the report to generating the structured Excel output.

### Previous Manual Process

```text
Email received
     ↓
Manually download Unstructured Data CSV
     ↓
Locate the downloaded file
     ↓
Manually create structured data CSV
     ↓
Use the generated file for further processing
```

### Automated Process
Outlook
   ↓
Power Automate
   ↓
OneDrive
   ↓
Local OneDrive Synchronization
   ↓
Windows Task Scheduler
   ↓
Python
   ↓
Structured Excel
   ↓
Processed CSV

## 2. Objective 
The primary objectives of the automation are to:
- Automatically identify the incoming AAI-44 report.
- Retrieve the CSV attachment from the email.
- Save the attachment to the configured OneDrive Input folder.
- Synchronize the file to the local Windows environment.
- Automatically execute the Python processing script.
- Transform the unstructured report into a structured dataset.
- Generate the required Excel output.
- Move the processed CSV to an archive folder.
- Eliminate human manual effort using agentic playbook and improve consistency of the daily reporting process.

## 3. Solution Architecture
The solution uses a hybrid cloud and local architecture.
┌──────────────────────┐
│      Outlook         │
│  AAI-44 Email Report │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│   Power Automate     │
│                      │
│ Validate attachment  │
│ and save CSV         │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│ OneDrive for Business│
│                      │
│ AAI44Input            │
└──────────┬───────────┘
           │
           │ OneDrive Sync
           ▼
┌──────────────────────┐
│   Windows Machine    │
│                      │
│ AAI44Input            │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│ Windows Task         │
│ Scheduler            │
│                      │
│ Executes Python      │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│       Python         │
│                      │
│ Read → Transform     │
│ → Generate Excel     │
└──────────┬───────────┘
           │
           ├──────────────────► AAI44Output
           │                     Structured Excel
           │
           ▼
     AAI44Processed
        Processed CSV

## 4.Technology Stack
| Technology | Purpose |
|---|---|
| Microsoft Outlook / Office 365 | Receives the daily AAI-44 report |
| Microsoft Power Automate       | Automates email and attachment processing |
| OneDrive for Business          | Stores and synchronizes the incoming CSV |
| Windows                        | Local execution environment |
| Windows Task Scheduler         | Automatically executes the Python process |
| Python                         | Processes and transforms the report |
| pandas                         | Data processing and transformation |
| openpyxl                       | Excel file generation |
| pathlib                        | File and path handling |
| os                             | File system operations |
| shutil                         | Moving processed files |
