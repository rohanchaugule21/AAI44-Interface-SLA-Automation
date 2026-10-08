# Testing and Validation

## 1. Overview

The AAI-44 Interface SLA Automation was tested end-to-end to validate the complete workflow from receiving the daily email report to generating the structured Excel output.

The testing covered both the cloud-based workflow and the local Windows-based processing components.

---

## 2. End-to-End Workflow Tested

The complete workflow tested was:

```text
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
Structured Excel Output
   ↓
Processed CSV
```

## 3. Test Environment
The automation was tested using the following components:
```
| Component                | Technology               |
|--------------------------|--------------------------|
| Email |                   Microsoft Outlook / Office 365 |
| Cloud workflow |          Microsoft Power Automate |
| File storage |            OneDrive for Business |
| Local environment |       Windows |
| Scheduling |              Windows Task Scheduler |
| Processing |              Python |
| Data processing |         pandas |
| Excel generation |        openpyxl |
```


## 4. Test Case 1 — Email Trigger
Objective
Verify that the Power Automate flow is triggered when the expected AAI-44 report email is received.
Test Conditions
The flow uses the following email criteria:
Sender:
```
OSS.Service.Assurance@sita.aero
```
Subject:
```
AAI-44 : Interface SLA Report - Hourly
```

Attachment:
CSV report containing the AAI-44 Interface SLA data.
Expected Result
Power Automate should detect the incoming email and start the workflow.
Result
Passed
The email trigger was successfully tested as part of the end-to-end automation.


## 5. Test Case 2 — Attachment Validation
Objective
Verify that the flow identifies the correct AAI-44 CSV attachment.
Validation Criteria
The attachment must satisfy:
```
Is Inline = false
AND
Name contains AAI-44
AND
Name ends with .csv
```

Expected Result
The valid AAI-44 CSV attachment should continue through the flow.
Invalid or unrelated attachments should not be processed.
Result
Passed
The attachment validation logic was successfully incorporated into the Power Automate workflow.


## 6. Test Case 3 — OneDrive File Creation
Objective
Verify that the validated CSV attachment is saved to the expected OneDrive folder.
Expected Location
```
AI Initiatives 2026/Agentic PlayBook/AAI44Input
```
Expected Result
Power Automate should create the CSV file in the OneDrive Input folder.
Result
Passed
The CSV attachment was successfully created in the configured OneDrive Input folder.


## 7. Test Case 4 — Local OneDrive Synchronization
Objective
Verify that the CSV saved by Power Automate becomes available in the local Windows Input folder.
Expected Local Location
```
C:\Users\<USERNAME>\OneDrive - SITA\AI Initiatives 2026\Agentic PlayBook\AAI44Input
```
Expected Result
The CSV should synchronize from OneDrive to the local machine.
Result
Passed
The CSV was successfully available in the local Input folder for Python processing.


## 8. Test Case 5 — Task Scheduler Execution
Objective
Verify that Windows Task Scheduler executes the Python automation.
Task Name
```
AAI44 Interface SLA Automation
```
Expected Result
The scheduled task should launch the configured Python script.
A successful Task Scheduler execution returns:
```
0x0
```
Result
Passed
The Task Scheduler task was manually executed during testing and completed successfully.
The task also showed a successful execution result:
```
Last Run Result: 0x0
```

## 9. Test Case 6 — Latest CSV Selection
Objective
Verify that the Python script automatically identifies the latest CSV file available in the Input folder.
Expected Result
The script should:
1. Search the AAI44Input folder.
2. Identify available CSV files.
3. Select the latest CSV based on file modification time.
4. Process the selected file.
Result
Passed
The automation successfully identified the available report for processing without requiring a manually specified input filename.


## 10. Test Case 7 — CSV Transformation
Objective
Verify that the unstructured AAI-44 report is transformed into a structured dataset.
Expected Output Columns
```
Airport
Timestamp
Current Utilization
CustomerKey
```
Transformation Validation
The Python process:
1. Reads the CSV file.
2. Identifies the airport/site from the report path.
3. Maintains the current airport/site while processing subsequent data rows.
4. Extracts the timestamp.
5. Extracts the current utilization value.
6. Adds the configured CustomerKey.
7. Creates the structured dataset.
Result
Passed
The report was successfully transformed into the required structured format.


## 11. Test Case 8 — Excel Generation
Objective
Verify that the transformed data is written to an Excel file.
Expected Output Location
```
AAI44Output
```
Expected Format
```
.xlsx
```
Expected Result
A structured Excel report should be generated from the processed CSV.
Result
Passed
The Excel output was successfully generated with the expected structured data.


## 12. Test Case 9 — Processed File Archiving
Objective
Verify that the input CSV is moved to the Processed folder after successful processing.
Expected Location
```
AAI44Processed
```

Expected Workflow
```
AAI44Input
    ↓
Python processing
    ↓
AAI44Output
    ↓
AAI44Processed
```
Result
Passed
The processed CSV was successfully moved to the Processed folder after the Excel output was generated.


## 13. End-to-End Test Result
The complete automation was tested from beginning to end.
Validation Flow
```
1. AAI-44 email received
        ↓
2. Power Automate triggered
        ↓
3. Attachment validated
        ↓
4. CSV saved to OneDrive
        ↓
5. CSV synchronized locally
        ↓
6. Task Scheduler executed
        ↓
7. Python identified the latest CSV
        ↓
8. CSV data transformed
        ↓
9. Excel output generated
        ↓
10. CSV moved to Processed
```

Overall Result
PASSED
The end-to-end automation successfully completed the expected workflow and generated the required structured Excel output.

## 14. Validation Summary
Test Area	                     Result
Email trigger	                  Passed
Attachment validation	         Passed
OneDrive file creation	         Passed
Local synchronization	         Passed
Task Scheduler execution	      Passed
Latest CSV selection	            Passed
CSV transformation	            Passed
Excel generation	               Passed
Processed file movement	         Passed
End-to-end workflow	            Passed


## 15. Acceptance Criteria
The automation is considered successfully validated when:
- The expected AAI-44 email is received.
- Power Automate processes the correct attachment.
- The CSV is saved to the OneDrive Input folder.
- The CSV becomes available locally.
- Windows Task Scheduler executes the Python process.
- Python identifies and processes the latest CSV.
- The report is transformed into the required structured format.
- The Excel output is generated successfully.
- The processed CSV is moved to the Processed folder.
All of the above were successfully validated during the end-to-end test.
