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
```
The script configuration contains:
```
BASE_FOLDER = r"...\Agentic PlayBook"
INPUT_FOLDER = os.path.join(BASE_FOLDER, "AAI44Input")
OUTPUT_FOLDER = os.path.join(BASE_FOLDER, "AAI44Output")
PROCESSED_FOLDER = os.path.join(BASE_FOLDER, "AAI44Processed")
```

The actual local Windows path is environment-specific and should not be hard-coded into shared documentation.

## 4. Customer Key
The automation uses the following CustomerKey:
```
1
```
The value is added to every structured output row.

5. Site / Airport Identification
The raw report contains path lines representing different Airport / Site values.
Examples include:
```
IXZ
HDO1
BOMH
MAAH
DBR_SDWAN
Azure
```
The Python function:
```
extract_site_name()
```

extracts the final path segment and uses it as the current Airport / Site.
The extracted site is then associated with subsequent data rows until another site path is encountered.

## 6. CSV Reading
The input file is opened in binary mode.
```
with open(input_file, 'rb') as f:
```

Each line is decoded using UTF-8 first.
If UTF-8 decoding fails, the script falls back to Latin-1.
```
try:
        line = raw_line.decode('utf-8').strip()
except
        UnicodeDecodeError:    line = raw_line.decode('latin1').strip()

```
This provides safer handling of files containing different character encodings.

## 7. Identifying Site Path Lines
The script checks whether a line:
- Starts with #
- Contains /
If the conditions are met, the final path segment is extracted as the site name.
Conceptually:
```
Report Path
     |
     v
Split by "/"
     |
     v
Take final segment
     |
     v
Airport / Site
```
For example:
```
.../IXZ
```
results in:
```
IXZ
```
Similarly:
```
.../DBR_SDWAN
```
results in:
```
DBR_SDWAN
```

## 8. Identifying Data Rows
Data rows are identified when:
- The line starts with a quotation mark.
- The character immediately after the quotation mark is a digit.
The script then splits the row by commas.
The first two relevant values are extracted as:
```
Timestamp
Current Utilization
```

## 9. Structured Output
For every valid data row, Python creates a structured record containing:
```
Airport
Timestamp
Current Utilization
CustomerKey
```

The resulting DataFrame uses the following column order:
```
Column	                                 Description
Airport	                                     Airport / Site identified from the report
Timestamp	                             Timestamp associated with the data row
Current Utilization	                     Utilization value from the report
CustomerKey	                             Customer identifier
```

## 10. Data Transformation
The transformation can be represented as:
```
Raw AAI-44 CSV
      |
      v
Identify Site
      |
      v
Identify Data Row
      |
      v
Extract Timestamp
      |
      v
Extract Current Utilization
      |
      v
Add CustomerKey
      |
      v
Structured DataFrame
```

## 11. Excel Generation
After all valid records have been collected, the script creates a pandas DataFrame.
The DataFrame is written to Excel using:
```
df.to_excel(    output_file,    index=False,    engine='openpyxl')
```

The generated file is stored in:
```
AAI44Output
```

The output filename is based on the input CSV filename.
For example:
```
Input:
AAI44_20261001_123512.csv

Output:
AAI44_20261001_123512.xlsx
```

## 12. Airport Count
After creating the DataFrame, the script calculates the number of unique Airport / Site values.
This is used in the processing status message:
```
Success! <rows> rows processed across <airports> airports.
```
This provides a basic processing summary.

## 13. Finding the Latest CSV
The Python automation searches the Input folder for CSV files.
```
Path(input_folder).glob("*.csv")
```

If no CSV files are available:
```
No CSV file found in AAI44Input.
Nothing to process.
```

The script then exits without generating an output file.
If multiple CSV files exist, the most recently modified CSV is selected.

## 14. Processing Sequence
The main Python workflow is:
```
Start
  |
  v
Create Required Folders
  |
  v
Find Latest CSV
  |
  +---- No CSV
  |       |
  |       v
  |      Exit
  |
  v
Create Output Filename
  |
  v
Transform CSV
  |
  +---- Error
  |       |
  |       v
  |   Keep CSV in Input
  |
  v
Verify Excel Exists
  |
  +---- No Excel
  |       |
  |       v
  |   Keep CSV in Input
  |
  v
Move CSV to Processed
  |
  +---- Move Failure
  |       |
  |       v
  |   Keep original CSV
  |
  v
Success
```

## 15. Error Handling
The script intentionally avoids moving the source CSV until successful processing has been confirmed.
Processing Failure
If the transformation raises an exception:
```
Python Processing
       |
       X
     Error
       |
       v
CSV remains in AAI44Input
```
This prevents a failed file from being incorrectly marked as processed.

Output Creation Failure
After transformation, the script checks whether the expected Excel file exists.
If the file does not exist:
```
ERROR: Output Excel was not created.
```
The CSV remains in the Input folder.

Processed File Move Failure
If the Excel file is successfully created but the CSV cannot be moved:
```
WARNING: Excel was created successfully,
but the CSV could not be moved to Processed.
```
The generated Excel remains available.

## 16. Successful Processing
When processing is successful:
```
AAI44Input
    |
    | CSV
    v
Python
    |
    +----> AAI44Output
    |        |
    |        └── Structured Excel
    |
    └----> AAI44Processed
             |
             └── Processed CSV
```

The final console output reports:
- Input CSV name
- Number of rows processed
- Output Excel name
- Processed CSV path

## 17. Python Dependencies
The Python script uses the following libraries:
pandas
Used for:
- Creating the structured DataFrame.
- Managing the transformed records.
- Exporting the structured dataset.

openpyxl
Used as the Excel engine when generating the .xlsx output.

os
Used for:
- Folder paths.
- Folder creation.
- File existence checks.

shutil
Used to move successfully processed CSV files.

pathlib
Used to search the Input folder and identify CSV files.

## 18. Execution Environment
The Python automation currently runs on the local Windows machine.
The Python executable is environment-specific.
The Task Scheduler configuration is responsible for launching the Python script.
The Python script itself does not contain Task Scheduler logic.


## 19. Separation of Responsibilities
The solution separates responsibilities between components:
```
Power Automate
    |
    +-- Receive and save report
    |
    v
OneDrive
    |
    +-- Synchronize file
    |
    v
Task Scheduler
    |
    +-- Launch Python
    |
    v
Python
    |
    +-- Transform data
    +-- Generate Excel
    +-- Archive CSV
```
This separation makes the solution easier to maintain and troubleshoot.

## 20. Important Implementation Principle
The Python transformation logic is the core processing component of the automation.
The tested implementation should be treated as the baseline version.
Any future changes to the transformation logic should be tested against representative AAI-44 report files before being deployed into the scheduled automation.

## 21. Current Limitation
Python execution currently depends on the local Windows environment.
The solution requires:
- Python to be available.
- Required Python packages to be installed.
- OneDrive synchronization to be available.
- The Windows machine to be available for scheduled execution.
A future implementation could move the Python execution to a cloud-hosted runtime if the operational requirement changes.

## 22. Summary
The Python automation converts the raw AAI-44 report into a structured Excel dataset while maintaining a clear input/output/processed file lifecycle.
```
Raw CSV
   |
   v
Latest File Selection
   |
   v
Site Identification
   |
   v
Data Extraction
   |
   v
Structured DataFrame
   |
   v
Excel Output
   |
   v
CSV Archive
```

The Python component removes the manual execution step from the original process while retaining the tested transformation logic.
