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