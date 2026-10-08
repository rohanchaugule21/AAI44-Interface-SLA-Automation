# AAI-44 Interface SLA Automation — Python Processing

## 1. Purpose

Python is responsible for transforming the raw AAI-44 Interface SLA CSV report into a structured Excel file.

The Python automation runs locally on the Windows machine and operates on files synchronized through OneDrive.

The Python script is intentionally kept separate from the Power Automate flow.

---

## 2. Python Responsibilities

The Python automation performs the following operations:

1. Creates the required runtime folders if they do not exist.
2. Searches the Input folder for CSV files.
3. Identifies the latest CSV file.
4. Reads the raw CSV safely.
5. Identifies the Airport / Site associated with each data row.
6. Extracts the timestamp.
7. Extracts the current utilization value.
8. Adds the CustomerKey.
9. Creates a structured pandas DataFrame.
10. Generates an Excel output file.
11. Verifies that the Excel file was created.
12. Moves the successfully processed CSV to the Processed folder.

---

## 3. Runtime Folder Configuration

The Python script uses a base folder and three runtime folders.

```text
Base Folder
│
├── AAI44Input
├── AAI44Output
└── AAI44Processed