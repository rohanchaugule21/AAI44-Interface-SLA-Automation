# AAI-44 Interface SLA Automation — Data Transformation

## 1. Purpose

The AAI-44 Interface SLA report is received as a CSV file containing report information in a semi-structured format.

The Python automation transforms this report into a structured dataset that can be consumed by downstream processes.

The transformation produces four output columns:

| Output Column | Source / Logic |
|---|---|
| Airport | Extracted from the report path |
| Timestamp | Extracted from the data row |
| Current Utilization | Extracted from the data row |
| CustomerKey | Static configured value |

---

## 2. Transformation Overview

The transformation follows:

```text
Raw AAI-44 CSV
      |
      v
Read file line-by-line
      |
      v
Identify Airport / Site
      |
      v
Identify Data Rows
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
      |
      v
Excel Output
```

## 3. Raw Report Structure
The input report contains multiple sections.
The report includes path information identifying the Airport / Site followed by data rows associated with that site.
Example site values include:
```
IXZ
HDO1
BOMH
MAAH
DBR_SDWAN
Azure
```
The Python script processes the file sequentially to maintain the relationship between a site path and its following data rows.


## 4. Site Identification
The function:
```
extract_site_name()
```
is responsible for identifying the Airport / Site from a report path.
A path line is recognized when:
```
The line starts with #
AND
The line contains /
```

The script then takes the final segment of the path.
For example:
```
.../IXZ
```
becomes:
```
IXZ
```

And:
```
.../DBR_SDWAN
```
becomes:
```
DBR_SDWAN
```


## 5. Current Airport State
The Python script maintains the current Airport / Site using:
```
current_airport
```

The initial value is:
```
Unknown
```

When a site path is encountered, current_airport is updated.
Subsequent data rows are assigned to that Airport / Site until another site path is encountered.
Conceptually:
```
Site Path: IXZ
      |
      +-- Data Row
      +-- Data Row
      +-- Data Row
      |
Site Path: HDO1
      |
      +-- Data Row
      +-- Data Row
      +-- Data Row
```
Therefore:
```
IXZ
  └── associated data rows

HDO1
  └── associated data rows
```


## 6. Data Row Identification
The script identifies a data row when:
```
The line starts with "
AND
The character immediately after " is a digit
```
This prevents metadata and other report lines from being treated as data rows.

## 7. Data Extraction
Once a valid data row is identified, the line is split using:
```
,
```
The script extracts the first two relevant values:
```
parts[0] → Timestamp
parts[1] → Current Utilization
```
Quotes and surrounding spaces are removed.


## 8. Output Record Creation
For every valid data row, the script creates a record:
```
{    'Airport': current_airport,
      'Timestamp': timestamp,
      'Current Utilization': utilization,
      'CustomerKey': customer_key}
```

These records are collected into a list.

## 9. Structured DataFrame
The collected records are converted into a pandas DataFrame with the following columns:
```
Airport
Timestamp
Current Utilization
CustomerKey
```
The column order is intentionally fixed.


## 10. CustomerKey
The automation uses:
```
CustomerKey = 1
```
The CustomerKey is added to every output record.
This value is configured in the Python script:
```
CUSTOMER_KEY = "1"
```

## 11. Example Transformation
Conceptually, a raw section of the report can be represented as:
```
Site Path
    |
    +-- Data Row
    +-- Data Row
    +-- Data Row
```
The transformation converts this into:
```
Airport	Timestamp	  Current Utilization	CustomerKey
IXZ	      Timestamp 1	  Utilization 1	          1
IXZ	      Timestamp 2	  Utilization 2	          1
IXZ	      Timestamp 3	  Utilization 3	          1

```
When the next site is encountered:
```
Airport	Timestamp	  Current Utilization	CustomerKey
HDO1	      Timestamp 4	   Utilization 4	          1
HDO1	      Timestamp 5	   Utilization 5	          1
```

The Airport value is therefore inherited from the most recent site path.


## 12. Encoding Handling
The input CSV is opened in binary mode.
The script first attempts UTF-8 decoding.
If UTF-8 decoding fails, the script falls back to Latin-1.
```
UTF-8
  |
  +-- Successful → Continue
  |
  +-- Failure
        |
        v
      Latin-1
```

This provides resilience when processing files containing characters that cannot be decoded using UTF-8.


## 13. Empty Lines and Metadata
Empty lines are ignored.
The script also does not treat arbitrary report metadata as data rows.
Only lines matching the expected data-row pattern are transformed into structured records.


## 14. Output Excel
After all valid records have been collected, the DataFrame is exported to Excel.
The output file uses the same base name as the input CSV.
```
Example:
Input:
AAI44_20261001_123512.csv

Output:
AAI44_20261001_123512.xlsx
```
The Excel file is stored in:
```
AAI44Output
```

## 15. Record Count
After the DataFrame is created, the automation calculates:
```
Number of processed rows
```
and:
```
Number of unique Airports / Sites
```
A success message is printed:
```
Success! <rows> rows processed across <airports> airports.
```
This provides a simple validation of the transformation.


## 16. Data Flow
The complete transformation can be summarized as:
```
                 RAW REPORT
                     |
                     v
              Read CSV Lines
                     |
                     v
             Identify Site Path
                     |
                     v
              Set Current Site
                     |
                     v
              Identify Data Row
                     |
                     v
          +----------+----------+
          |                     |
          v                     v
      Timestamp          Current Utilization
          |                     |
          +----------+----------+
                     |
                     v
              Add CustomerKey
                     |
                     v
             Structured Record
                     |
                     v
               DataFrame
                     |
                     v
                 Excel
```

## 17. Data Quality Considerations
The transformation relies on the expected structure of the AAI-44 report.
Important assumptions include:
- Site information is present in the expected path format.
- Data rows follow the expected quoted format.
- Timestamp is the first relevant field.
- Current Utilization is the second relevant field.
- Site path lines occur before their associated data rows.
If the upstream report format changes, the transformation logic should be reviewed and tested.


## 18. Handling Unknown Site
The initial Airport / Site value is:
```
Unknown
```
If a valid data row is encountered before a site path has been identified, the row can therefore receive:
```
Airport = Unknown
```
This provides a visible indication that the expected site information was not available before the data row.


## 19. No Data Modification Beyond Required Transformation
The Python script performs the required structural transformation.
It does not perform business calculations or modify the utilization values.
The main transformation is:
```
Semi-structured report
        ↓
Structured records
```
The source Timestamp and Current Utilization values are extracted and placed into the corresponding output columns.


## 20. Output Schema
The final Excel schema is:
```
+----------------------+------------------------------+
| Column               | Description                  |
+----------------------+------------------------------+
| Airport              | Airport / Site               |
| Timestamp            | Source timestamp             |
| Current Utilization  | Source utilization value     |
| CustomerKey          | Configured customer key      |
+----------------------+------------------------------+
```

## 21. Transformation Dependency
The transformation depends on the structure of the AAI-44 report received from the upstream source.
Changes to the following could require code changes:
- Report path structure.
- Site identification format.
- Data row format.
- Field ordering.
- CSV encoding.
- Required output columns.
Any upstream report format change should therefore be validated before the automation is considered production-ready.


## 22. Summary
The Python transformation converts the semi-structured AAI-44 Interface SLA report into a consistent four-column structured dataset.
```
Raw AAI-44 Report
        |
        v
Site Identification
        |
        v
Data Row Extraction
        |
        v
Timestamp + Utilization
        |
        v
CustomerKey
        |
        v
Structured Excel
```

