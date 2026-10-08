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
```
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
```

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

## 5. End-to-End Workflow 
Step 1 — Receive Report
The daily AAI-44 Interface SLA report is received through Outlook.
The Power Automate flow identifies the email using the configured sender and subject.

Step 2 — Validate Attachment
Power Automate validates the attachment using:
Is Inline = false
AND
Name contains AAI-44
AND
Name ends with .csv
Only attachments satisfying the validation criteria are processed.

Step 3 — Save CSV
The validated CSV is saved to:
AI Initiatives 2026/Agentic PlayBook/AAI44Input
in OneDrive for Business.

Step 4 — Synchronize Locally
OneDrive synchronizes the CSV to the local Windows machine.

Step 5 — Execute Python
Windows Task Scheduler executes the Python automation.
The Python process identifies the latest CSV available in the Input folder.

Step 6 — Transform Data
Python reads the report and extracts:
- Airport / Site
- Timestamp
- Current Utilization
- CustomerKey
The unstructured report is converted into a structured dataset.

Step 7 — Generate Excel
The structured data is written to an Excel file in:
AAI44Output

Step 8 — Archive Processed CSV
After successful processing, the original CSV is moved from:
AAI44Input
to:
AAI44Processed

## 6. Folder Structure
The runtime folder structure is:
```
Agentic PlayBook/
│
├── Automation.py
│
├── AAI44Input/
│   └── Incoming CSV files
│
├── AAI44Output/
│   └── Generated Excel files
│
└── AAI44Processed/
    └── Successfully processed CSV files
```

## 7. Repository Structure
```
AAI44-Interface-SLA-Automation/
│
├── README.md
│
├── src/
│   └── Automation.py
│
├── docs/
│   ├── 01-Solution-Overview.md
│   ├── 02-Architecture.md
│   ├── 03-Power-Automate.md
│   ├── 04-OneDrive-Integration.md
│   ├── 05-Python-Processing.md
│   ├── 06-Task-Scheduler.md
│   ├── 07-Data-Transformation.md
│   ├── 08-Error-Handling-and-Troubleshooting.md
│   └── 09-Testing-and-Validation.md
│
├── diagrams/
│   └── architecture.png
│
├── examples/
│   └── README.md
│
└── .gitignore
```

## 8. Python Processing
The Python script performs the core data transformation.
```
Find latest CSV
      ↓
Read report
      ↓
Identify airport/site
      ↓
Extract timestamp
      ↓
Extract utilization
      ↓
Add CustomerKey
      ↓
Create structured DataFrame
      ↓
Generate Excel
      ↓
Move CSV to Processed
```

Output Schema
Column	          Description
Airport	          Airport/site identified from the report path
Timestamp	          Timestamp extracted from the report
Current Utilization	Utilization value from the report
CustomerKey	     Customer identifier configured for the process

## 9. Key Benefits
Reduced Manual Effort:
The previous process required manual downloading of the report and manual execution of the Python script.
The automated workflow removes these repetitive activities.

Consistent Processing:
The same validation and transformation logic is executed for each incoming report.

Automated File Management:
Files are automatically separated into: 
```
Input
Output
Processed
```

## 10. External Dependencies
The current implementation depends on:
- Microsoft Outlook / Office 365
- Microsoft Power Automate
- OneDrive for Business
- Windows machine
- Windows Task Scheduler
- Python runtime
- pandas
- openpyxl
- Network connectivity for cloud services and OneDrive synchronization
The current solution does not require:
- Azure Functions
- SharePoint storage
- A separate cloud-hosted Python service

## 11. Current Architecture Consideration
The current implementation is a hybrid cloud/local solution.
Power Automate and OneDrive handle the cloud-based portion of the workflow, while Windows Task Scheduler and Python handle local processing.
Therefore, the local Windows machine must be available for the scheduled Python process to execute.
If the machine is completely powered off, Windows Task Scheduler cannot execute the Python process.
This is a known characteristic of the current implementation.

## 12. Security and Data Considerations
The repository should contain only source code and technical documentation.
The following should not be committed to GitHub:
- Customer CSV files
- Generated Excel reports
- Email attachments
- Passwords
- Access tokens
- Client secrets
- Other confidential configuration information
The .gitignore file excludes generated CSV and Excel files as well as common local configuration and runtime files.
Local Windows paths should be represented using placeholders such as:
```
C:\Users\<USERNAME>\...
```

## 13. Testing and Validation
The solution was tested end-to-end.
The following stages were successfully validated:
```
Email received
      ↓
Power Automate triggered
      ↓
Attachment validated
      ↓
CSV saved to OneDrive
      ↓
CSV synchronized locally
      ↓
Task Scheduler executed
      ↓
Python processed CSV
      ↓
Excel generated
      ↓
CSV moved to Processed
```
Overall Test Result: 
The complete workflow successfully generated the expected structured Excel output.
Detailed testing information is available in:
docs/09-Testing-and-Validation.md

## 14. Documentation
Detailed documentation is available in the docs folder.
```
| Document                                            | Description |
|---------------------------------------------------|----------------------------------------------------------|
| 01-Solution-Overview.md                           | Overall solution and objective |
| 02-Architecture.md                                | Architecture and component responsibilities |
| 03-Power-Automate.md                              | Power Automate flow configuration |
| 04-OneDrive-Integration.md                        | OneDrive integration and synchronization |
| 05-Python-Processing.md                           | Python processing logic |
| 06-Task-Scheduler.md                              | Windows Task Scheduler configuration |
| 07-Data-Transformation.md                         | Report transformation logic |
| 08-Error-Handling-and-Troubleshooting.md          | Troubleshooting and recovery guidance |
| 09-Testing-and-Validation.md                      | End-to-end testing and validation |
```

## 15. Future Improvements
Potential future improvements include:
- Moving Python execution to a cloud-based execution environment.
- Removing dependency on a local Windows machine.
- Adding centralized execution logging.
- Adding automated failure notifications.
- Adding monitoring for missing daily reports.
- Adding retry handling for transient failures.
- Further integrating the automation into the broader cloud environment.

The enhancements described in this section are potential future improvements and are **not part of the current implementation**. These enhancements may introduce additional costs depending on the services and resources required.
To avoid unnecessary costs at this stage, the current architecture has been designed with these potential enhancements in mind, while keeping them outside the scope of the present implementation. The architecture can be extended in the future if these capabilities are required.
