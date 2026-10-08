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