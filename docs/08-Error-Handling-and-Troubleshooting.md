# AAI-44 Interface SLA Automation — Error Handling & Troubleshooting

## 1. Purpose

This document describes the main failure scenarios in the AAI-44 agentic playbook automation and provides troubleshooting guidance for each component.

The automation consists of multiple stages:

```text
Outlook
   |
   v
Power Automate
   |
   v
OneDrive
   |
   v
Windows / OneDrive Sync
   |
   v
Task Scheduler
   |
   v
Python
   |
   +----> Excel Output
   |
   +----> Processed CSV
   
   
A failure in any component can prevent the final Excel report from being generated.
This document provides troubleshooting guidance for identifying and resolving failures in the automation workflow.
```

## 2. Troubleshooting Approach
When the expected Excel output is not available, troubleshoot the workflow from the beginning of the data flow.
Recommended order:
1. Check whether the email was received.
2. Check whether Power Automate was triggered.
3. Check whether the attachment passed the validation condition.
4. Check whether the CSV was created in the OneDrive Input folder.
5. Check whether the CSV synchronized to the local machine.
6. Check whether Windows Task Scheduler executed the Python script.
7. Check the Python execution output.
8. Check whether the Excel file was generated.
9. Check whether the processed CSV was moved to the Processed folder.
This approach helps identify the failed component without manually checking every part of the solution.


## 3. Outlook / Email Troubleshooting
Problem
The expected AAI-44 report is not available in the Input folder.
Checks
Verify that the daily email was received in Outlook.
The automation expects:
Sender:
OSS.Service.Assurance@sita.aero
Subject:
AAI-44 : Interface SLA Report - Hourly

The email should also contain an attachment.
Possible Causes
- Email was not received.
- Sender or subject has changed.
- Email arrived later than expected.
- Attachment was not included.
- Outlook/mailbox connectivity issue.
Resolution
Confirm that the email exists in Outlook and that the sender, subject, and attachment are correct.
If the email itself was not received, Power Automate cannot process the report.

## 4. Power Automate Troubleshooting
Problem
The email was received, but no CSV appears in the OneDrive Input folder.
Check Flow Run History
Open the Power Automate flow and check Run History.
Confirm that the flow was triggered by the expected email.
Check the following actions:
1. When a new email arrives (V3)
2. Apply to each
3. Get Attachment (V2)
4. Attachment validation condition
5. Compose actions
6. OneDrive - Create file

## 5. Attachment Validation Troubleshooting
The flow validates the attachment before saving it.
The validation checks:
Is Inline = false
AND
Name contains AAI-44
AND
Name ends with .csv

Possible Causes
If the condition evaluates to False, the attachment will not be saved.
Possible reasons include:
- Attachment is an inline attachment.
- Attachment name does not contain AAI-44.
- Attachment is not a .csv file.
- Attachment metadata is different from the expected format.
Resolution
Open the Get Attachment (V2) action and verify:
-Is Inline
-Name
-Content Bytes
Confirm that the attachment satisfies all three validation conditions.

## 6. OneDrive Troubleshooting
Problem
Power Automate completed successfully, but the CSV is not visible locally.
Check Cloud OneDrive
First verify that the file exists in:
AI Initiatives 2026/Agentic PlayBook/AAI44Input
If the file is present in OneDrive but not visible locally, the issue is likely related to OneDrive synchronization.
Check Local Folder
The local folder is:
C:\Users\<USERNAME>\OneDrive - SITA\AI Initiatives 2026\Agentic PlayBook\AAI44Input

Verify that the CSV appears in this folder.
Possible Causes
- OneDrive synchronization is delayed.
- OneDrive is paused.
- Network connectivity is unavailable.
- OneDrive client is not running.
- Local OneDrive folder is unavailable.
Resolution
Confirm that OneDrive is running and synchronized before expecting the Python process to find the CSV.

## 7.Task Scheduler Troubleshooting
Problem
The CSV exists locally, but the Excel output is not generated.
Open:
Task Scheduler

Locate:
AAI44 Interface SLA Automation

Check:
- Last Run Time
- Last Run Result
- Next Run Time
- Task status
A successful Task Scheduler execution normally shows:
Last Run Result: 0x0

Possible Causes
- Task did not run.
- Task was disabled.
- Computer was switched off.
- Scheduled execution was missed.
- Task Scheduler configuration is incorrect.
- Python action configuration is incorrect.

## 8. Python Execution Troubleshooting
Problem
Task Scheduler runs, but the Excel file is not created.
Verify the Task Scheduler action.
Program/script
C:\Users\<USERNAME>\AppData\Local\Microsoft\WindowsApps\python.exe

Add arguments
"C:\Users\<USERNAME>\OneDrive - SITA\AI Initiatives 2026\Agentic PlayBook\Automation.py"

Start in
C:\Users\<USERNAME>\OneDrive - SITA\AI Initiatives 2026\Agentic PlayBook

The Start in field should point to the directory containing the Python script.

## 9. No CSV Found
The Python script searches the Input folder for CSV files.
If no CSV exists, the script displays:
No CSV file found in AAI44Input.
Nothing to process.

Possible Causes
- Power Automate did not save the attachment.
- OneDrive synchronization has not completed.
- CSV was already moved to the Processed folder.
- Input folder is incorrect.
Resolution
Check:
AAI44Input

and verify that a .csv file is present.

## 10. Latest File Selection
The Python automation identifies the latest CSV file in the Input folder based on the file's modification time.
This allows the scheduled process to select the most recent available report without requiring a fixed filename.
If multiple CSV files are present, the latest modified CSV is selected for processing.

## 11. Excel Output Troubleshooting
The expected output is generated in:
AAI44Output

The output filename is based on the processed CSV filename.
For example:
AAI44_20260930_123500.csv

produces:
AAI44_20260930_123500.xlsx

Possible Causes
- Python processing failed.
- Input CSV format changed.
- Output folder is unavailable.
- Required Python libraries are unavailable.
- Excel file is already locked by another process.
Resolution
Check the Python execution output and verify the Input and Output folder paths.

## 12. Processed Folder Troubleshooting
After successful Excel generation, the input CSV is moved to:
AAI44Processed

Example:
AAI44Input
    ↓
Python processing
    ↓
AAI44Output
    ↓
AAI44Processed

If the Excel file is successfully created but the CSV remains in AAI44Input, the processing succeeded but the file move operation failed.
The Python script reports this as a warning.

## 13. Duplicate Processing
The automation is designed to reduce duplicate processing by moving the successfully processed CSV from:
AAI44Input

to:
AAI44Processed

Once moved, the CSV is no longer available in the Input folder for the next scheduled execution.
The Task Scheduler configuration also uses:
If the task is already running:
Do not start a new instance

This helps prevent overlapping executions.

## 14. Laptop Availability
The current implementation uses a local Windows machine for Python execution.
Therefore, the machine must be available for the scheduled task to execute.
The solution can work while the machine is running and the required services are available.
If the laptop is completely powered off, Windows Task Scheduler cannot execute the Python process.
Optional Task Scheduler settings can be used to improve handling of sleep or missed schedules, including:
Wake the computer to run this task

and:
Run task as soon as possible after a scheduled start is missed

These settings should be enabled only if they are appropriate for the local machine and organizational policies.

## 15. Summary
If the automation does not produce the expected Excel report, use the following checklist:
[ ] Email received
[ ] Correct sender
[ ] Correct subject
[ ] Attachment exists
[ ] Power Automate flow triggered
[ ] Attachment validation succeeded
[ ] CSV created in OneDrive
[ ] CSV synchronized locally
[ ] CSV available in AAI44Input
[ ] Task Scheduler executed
[ ] Last Run Result checked
[ ] Python script executed
[ ] Excel created in AAI44Output
[ ] CSV moved to AAI44Processed

Email
  ↓
Power Automate
  ↓
OneDrive
  ↓
Local Input
  ↓
Task Scheduler
  ↓
Python
  ↓
Output Excel
  ↓
Processed CSV