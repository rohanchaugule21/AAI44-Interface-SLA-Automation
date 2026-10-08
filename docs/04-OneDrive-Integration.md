# AAI-44 Interface SLA Automation — OneDrive Integration

## 1. Purpose

OneDrive for Business is used as the file transfer and synchronization layer between the Power Automate cloud flow and the local Windows environment.

Power Automate saves the incoming AAI-44 CSV into a OneDrive folder.

The OneDrive client then synchronizes the file to the local Windows machine, where Windows Task Scheduler and Python can access it.

---

## 2. Integration Flow

The integration follows this path:

```text
Power Automate
      |
      | Create file
      v
OneDrive for Business
      |
      | OneDrive synchronization
      v
Local Windows Folder
      |
      v
Windows Task Scheduler
      |
      v
Python Automation
```

## 3. OneDrive Cloud Folder
Power Automate creates the incoming CSV in:
```
/AI Initiatives 2026/Agentic PlayBook/AAI44Input
```

The Power Automate action used is:
```
OneDrive for Business — Create file
```

The file name is generated dynamically by Power Automate.
Example:
```
AAI44_20261001_123512.csv
```

## 4. Local Folder
The OneDrive folder is synchronized to the local Windows machine.
The local Input folder is:
```
C:\Users\<USERNAME>\OneDrive - SITA\AI Initiatives 2026\Agentic PlayBook\AAI44Input
```
The actual runtime environment uses the user's local Windows profile.
For shared documentation, <USERNAME> should be used instead of publishing a personal local path.

## 5. Local Runtime Folder Structure
The complete local runtime structure is:
```
Agentic PlayBook
│
├── Automation.py
│
├── AAI44Input
│   └── Incoming CSV files
│
├── AAI44Output
│   └── Generated Excel files
│
└── AAI44Processed
    └── Successfully processed CSV files
```

## 6. Input Folder
The AAI44Input folder is the handoff location between OneDrive and the Python automation.
Power Automate writes the CSV to the OneDrive cloud folder.
OneDrive synchronizes the file to the local AAI44Input folder.
Example:
```
Cloud:
AI Initiatives 2026/Agentic PlayBook/AAI44Input

              |
              | OneDrive Sync
              v

Local:
OneDrive - SITA\AI Initiatives 2026\Agentic PlayBook\AAI44Input
```

## 7. File Naming
Power Automate generates a timestamp-based file name.
Format:
```
AAI44_YYYYMMDD_HHMMSS.csv
```
Example:
```
AAI44_20261001_123512.csv
```
The timestamp is generated from the email received date and time.
This provides a unique file name for each report and avoids relying on the original attachment name.

## 8. Why OneDrive Is Used
OneDrive was selected because it provides a simple bridge between the cloud Power Automate flow and the local Windows execution environment.
The approach avoids introducing an additional cloud-hosted Python service.
The current implementation therefore does not require:
- Azure Function
- SharePoint
- Separate file transfer service
- Application server
- Cloud-hosted Python execution environment

## 9. File Lifecycle
The file lifecycle is:
```
Email Attachment
       |
       v
Power Automate
       |
       v
OneDrive Cloud
       |
       v
Local AAI44Input
       |
       v
Python Processing
       |
       +------------------+
       |                  |
       v                  v
AAI44Output        AAI44Processed
Excel Output       Processed CSV
```

The CSV is initially available in AAI44Input.
After successful processing, Python moves the CSV to AAI44Processed.
The generated Excel remains in AAI44Output.

## 10. Synchronization Dependency
The local automation depends on OneDrive synchronization being available.
The expected sequence is:
```
1. Power Automate creates CSV
2. OneDrive receives the file
3. OneDrive synchronizes the file locally
4. CSV becomes available in AAI44Input
5. Task Scheduler starts Python
6. Python finds the latest CSV
7. Python processes the CSV
```
If the file has not synchronized to the local machine when Python executes, Python may not find the expected CSV.

## 11. Interaction with Python
Python does not access the OneDrive cloud API directly.
Instead, Python reads the local synchronized folder.
The Python automation checks:
```
AAI44Input
```
and identifies the most recently modified CSV.
This keeps the Python component independent from the Power Automate implementation.

## 12. Interaction with Task Scheduler
Task Scheduler launches the Python script.
Python then checks the local OneDrive-synchronized Input folder.
```
Task Scheduler
      |
      v
Automation.py
      |
      v
Local OneDrive
AAI44Input
      |
      v
Latest CSV
```
The scheduler therefore does not need to know the name of the incoming CSV.
The Python script determines which CSV should be processed.

## 13. Failure Scenarios
Scenario 1 — Power Automate fails
If Power Automate fails to create the file:
```
Email
  |
  X
Power Automate
```
No local CSV will be available.
Python will have nothing to process.

Scenario 2 — OneDrive synchronization is delayed
If Power Automate successfully creates the file but OneDrive has not synchronized it locally:
```
Power Automate
      |
      v
OneDrive Cloud
      |
      X
Local Folder
```
Python may not find the CSV during that execution.

Scenario 3 — Python processing fails
If the CSV is available locally but Python fails during processing:
```
AAI44Input
     |
     v
Python
     |
     X
Processing Error
```
The CSV remains in AAI44Input.
It is not moved to AAI44Processed.
This allows investigation and reprocessing.

## 14. Operational Considerations
The local Windows machine is an important part of the current architecture.
The machine must be available for:
- OneDrive synchronization
- Windows Task Scheduler
- Python execution
The current solution is therefore a hybrid cloud/local implementation rather than a fully cloud-hosted automation.

## 15. Security Considerations
The OneDrive folders may contain operational/customer report data.
The following should not be committed to GitHub:
```
*.csv
*.xlsx
```

The repository .gitignore excludes these file types.
The GitHub repository should contain:
- Source code
- Documentation
- Architecture information
- Configuration guidance
- Troubleshooting information
It should not contain actual customer report data.

## 16. Summary
OneDrive provides the file-based integration layer between Power Automate and the local Python automation.
```
Power Automate
      |
      v
OneDrive Cloud
      |
      | Sync
      v
Local AAI44Input
      |
      v
Task Scheduler
      |
      v
Python
      |
      +----> AAI44Output
      |
      +----> AAI44Processed
```

This approach allows the existing Python transformation logic to be retained while removing the manual step of downloading the daily AAI-44 report.

Your repository should now be:
```
AAI44-Interface-SLA-Automation
│
├── .gitignore
│
├── src/
│   └── Automation.py
│
├── docs/
│   ├── 01-Solution-Overview.md
│   ├── 02-Architecture.md
│   ├── 03-Power-Automate.md
│   └── 04-OneDrive-Integration.md
│
├── diagrams/
│
└── examples/
```
