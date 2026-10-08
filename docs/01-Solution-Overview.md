# AAI-44 Interface SLA Automation

## 1. Overview

In the AAI IRS Project, we have AAI44 reporting solution where we have multiple reports in the Power Bi app. Out of these multiple reports, we have a report named Bandwidth Utilization report. For this report we receive data from Ngoss the source from where we consume the data and apply business logic to show the data on the power bi dashboard.
 
The AAI44 Reporting Solution (within the AAI IRS Project) provides critical Bandwidth Utilization insights via Power BI. Data is primarily sourced from Ngoss and processed through APIs and database business logic to populate the Power Bi dashboard.
Frequent data gaps at the source (Ngoss) result in missing records within the API. To compensate, the Ngoss team provides raw, unstructured Excel files for 45 different airports for the missed days. The Challenge here is manually structuring this data for database consumption is labor-intensive, consuming multiple man-hours per day and increasing the risk of human error.

The automation combines Microsoft Power Automate, OneDrive for Business, Windows Task Scheduler, and Python to create an end-to-end automated workflow.

---

## 2. Business / Technical Objective

The objective of this automation is to:

- Automatically capture the daily AAI-44 Interface SLA Report.
- Save the incoming CSV file without manual intervention.
- Automatically identify and process the latest report.
- Transform the unstructured report into a structured dataset.
- Generate an Excel output file containing the required AAI-44 data.
- Archive the successfully processed CSV file.
- Eliminate manual operational effort using agentic playbook and improve processing consistency.

---

## 3. Solution Architecture

The overall workflow is:

```text
Outlook
   |
   v
Power Automate Cloud Flow
   |
   | Extract and validate CSV attachment
   v
OneDrive for Business
   |
   | OneDrive synchronization
   v
Local Windows Machine
   |
   v
Windows Task Scheduler
   |
   v
Python Automation
   |
   +--> Read latest CSV
   |
   +--> Identify Airport / Site
   |
   +--> Extract Timestamp
   |
   +--> Extract Current Utilization
   |
   +--> Add CustomerKey
   |
   v
Structured Excel Output
   |
   v
Processed CSV Archive
```

## 4. Components
Microsoft Outlook / Office 365: 
The daily AAI-44 Interface SLA Report is received through the SITA Outlook mailbox.
The automation uses the email sender and subject to identify the expected report.

Microsoft Power Automate: 
Power Automate monitors incoming emails and processes the attachments.
The flow:
1. Detects the incoming AAI-44 report email.
2. Checks that the email contains attachments.
3. Retrieves the attachment.
4. Validates that the attachment is not inline.
5. Validates the expected AAI-44 file name.
6. Validates that the file is a CSV.
7. Creates a timestamped file name.
8. Saves the CSV into the OneDrive input folder.

OneDrive for Business:
OneDrive acts as the bridge between the cloud-based Power Automate flow and the local Windows environment.
The CSV is initially stored in:
```
AI Initiatives 2026/Agentic PlayBook/AAI44Input
```
OneDrive synchronizes this folder with the local Windows machine.

Windows Task Scheduler: 
Windows Task Scheduler executes the Python automation at the configured schedule.
The current implementation checks the input folder and processes the latest available CSV file.

Python:
Python performs the actual transformation of the AAI-44 report.
The script:
1. Finds the latest CSV file.
2. Reads the report safely.
3. Identifies the Airport / Site from the report path.
4. Extracts timestamp and utilization information.
5. Adds the CustomerKey.
6. Creates a structured dataset.
7. Generates an Excel output file.
8. Moves the successfully processed CSV into the Processed folder.

## 5. Input
The input is the daily AAI-44 Interface SLA Report received as a CSV email attachment.
The CSV contains report information including site paths and utilization data.
The automation does not require the user to manually download the attachment.

## 6. Output
The automation generates an Excel file containing the structured data:
```
Column	                                              Description
Airport	                                                 Airport / Site identified from the report path
Timestamp	                                         Timestamp associated with the utilization record
Current Utilization	                                 Current utilization value
CustomerKey	                                         Customer identifier used by the solution
```

The generated Excel file is stored in:
```
AAI44Output
```

## 7. File Processing Lifecycle
The solution uses three folders:
```
AAI44Input
     |
     | Latest CSV selected
     v
Python Processing
     |
     +----> AAI44Output
     |       Structured Excel
     |
     v
AAI44Processed
        Successfully processed CSV
```

AAI44Input: 
Contains CSV files received from the Power Automate flow.

AAI44Output:
Contains the generated structured Excel files.

AAI44Processed:
Contains CSV files that were successfully processed.
If Python processing fails, the CSV is not moved to the Processed folder. This allows the input file to remain available for investigation.

## 8. Error Handling
The Python automation includes checks for:
- No CSV file available.
- Python processing failure.
- Output Excel not being created.
- Failure to move the processed CSV.
The CSV is retained in the Input folder if processing fails, allowing the issue to be investigated and the file to be processed again.

## 9. Technology Stack
- Microsoft Outlook / Office 365
- Microsoft Power Automate Cloud
- Microsoft OneDrive for Business
- Microsoft Windows
- Windows Task Scheduler
- Python
- pandas
- openpyxl
- os
- shutil
- pathlib
