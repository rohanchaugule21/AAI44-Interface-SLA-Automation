import pandas as pd
import os
import shutil
from pathlib import Path


# ============================================================
# CONFIGURATION
# ============================================================

BASE_FOLDER = r"C:\Users\Rohan.Chaugule\OneDrive - SITA\AI Initiatives 2026\Agentic PlayBook"

INPUT_FOLDER = os.path.join(BASE_FOLDER, "AAI44Input")
OUTPUT_FOLDER = os.path.join(BASE_FOLDER, "AAI44Output")
PROCESSED_FOLDER = os.path.join(BASE_FOLDER, "AAI44Processed")

CUSTOMER_KEY = "1"


# ============================================================
# HELPERS
# ============================================================

def extract_site_name(line):
    """
    Path lines look like:
        #"All/AAI45 - IRS Reports/AAI-44 : Interface SLA Report - Hourly/IXZ"
        #"All/AAI45 - IRS Reports/AAI-44 : Interface SLA Report - Hourly/BOMH"
        #"All/AAI45 - IRS Reports/AAI-44 : Interface SLA Report - Hourly/DBR_SDWAN"
        #"All/AAI45 - IRS Reports/AAI-44 : Interface SLA Report - Hourly/Azure"

    Returns the last path segment (the site name), whatever its
    length or characters. Returns None if the line is not a path line.
    """
    if not line.startswith("#") or "/" not in line:
        return None

    # Only treat lines that belong to the report path as site lines.
    # (The date line, e.g. #"September 2026, from Monday 28 ...", has no "/")
    site = line.rstrip("\"' ").split("/")[-1].strip()

    return site if site else None


# ============================================================
# AAI-44 CSV TRANSFORMATION
# ============================================================

def transform_airport_data(input_file, output_file, customer_key):

    structured_rows = []
    current_airport = "Unknown"

    # Opening in binary mode and decoding manually
    # handles mixed encodings safely
    with open(input_file, 'rb') as f:

        for raw_line in f:

            try:
                line = raw_line.decode('utf-8').strip()

            except UnicodeDecodeError:
                line = raw_line.decode('latin1').strip()

            # 1. Skip empty lines/gaps
            if not line:
                continue

            # 2. Extract site name from the path line
            #    (works for IXZ, HDO1, BOMH, MAAH, DBR_SDWAN, Azure, ...)
            site = extract_site_name(line)

            if site:
                current_airport = site
                continue

            # 3. Identify Data Rows
            # Data rows start with a quote followed by a digit
            if line.startswith('"') and len(line) > 1 and line[1].isdigit():

                parts = line.split(',')

                if len(parts) >= 2:

                    # Remove quotes and clean spaces
                    timestamp = parts[0].strip('" ')
                    utilization = parts[1].strip('" ')

                    structured_rows.append({
                        'Airport': current_airport,
                        'Timestamp': timestamp,
                        'Current Utilization': utilization,
                        'CustomerKey': customer_key
                    })

    # Create DataFrame with the expected columns
    df = pd.DataFrame(
        structured_rows,
        columns=[
            'Airport',
            'Timestamp',
            'Current Utilization',
            'CustomerKey'
        ]
    )

    # Export to Excel
    df.to_excel(
        output_file,
        index=False,
        engine='openpyxl'
    )

    # Calculate number of unique airports/sites
    airport_count = df['Airport'].nunique()

    print(
        f"Success! {len(df)} rows processed "
        f"across {airport_count} airports."
    )

    # Return number of processed rows
    return len(df)


# ============================================================
# FIND LATEST CSV FILE
# ============================================================

def get_latest_csv(input_folder):

    csv_files = list(
        Path(input_folder).glob("*.csv")
    )

    # No CSV found
    if not csv_files:
        return None

    # Find the most recently modified CSV
    latest_file = max(
        csv_files,
        key=lambda file: file.stat().st_mtime
    )

    return latest_file


# ============================================================
# MAIN AUTOMATION
# ============================================================

def main():

    print("=" * 60)
    print("AAI-44 Interface SLA Automation")
    print("=" * 60)

    # --------------------------------------------------------
    # 1. Make sure required folders exist
    # --------------------------------------------------------

    os.makedirs(INPUT_FOLDER, exist_ok=True)
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    os.makedirs(PROCESSED_FOLDER, exist_ok=True)

    print(f"Input folder:     {INPUT_FOLDER}")
    print(f"Output folder:    {OUTPUT_FOLDER}")
    print(f"Processed folder: {PROCESSED_FOLDER}")
    print()

    # --------------------------------------------------------
    # 2. Find latest CSV
    # --------------------------------------------------------

    latest_csv = get_latest_csv(INPUT_FOLDER)

    if latest_csv is None:

        print("No CSV file found in AAI44Input.")
        print("Nothing to process.")
        return

    print("Latest CSV found:")
    print(latest_csv)
    print()

    # --------------------------------------------------------
    # 3. Create output Excel filename
    # --------------------------------------------------------

    output_filename = latest_csv.stem + ".xlsx"

    output_file = os.path.join(
        OUTPUT_FOLDER,
        output_filename
    )

    print("Output Excel:")
    print(output_file)
    print()

    # --------------------------------------------------------
    # 4. Run the AAI-44 transformation
    # --------------------------------------------------------

    try:

        rows_processed = transform_airport_data(
            str(latest_csv),
            output_file,
            CUSTOMER_KEY
        )

    except Exception as e:

        print("=" * 60)
        print("ERROR: Python processing failed.")
        print("=" * 60)
        print(str(e))

        # Do NOT move the CSV to Processed
        # because processing failed.
        return

    # --------------------------------------------------------
    # 5. Verify the Excel was created
    # --------------------------------------------------------

    if not os.path.exists(output_file):

        print("=" * 60)
        print("ERROR: Output Excel was not created.")
        print("=" * 60)

        # Keep CSV in Input for investigation
        return

    # --------------------------------------------------------
    # 6. Move successfully processed CSV
    # --------------------------------------------------------

    processed_file = os.path.join(
        PROCESSED_FOLDER,
        latest_csv.name
    )

    try:

        shutil.move(
            str(latest_csv),
            processed_file
        )

    except Exception as e:

        print("=" * 60)
        print("WARNING: Excel was created successfully,")
        print("but the CSV could not be moved to Processed.")
        print("=" * 60)
        print(str(e))

        return

    # --------------------------------------------------------
    # 7. Final success message
    # --------------------------------------------------------

    print()
    print("=" * 60)
    print("AAI-44 AUTOMATION COMPLETED SUCCESSFULLY")
    print("=" * 60)
    print(f"Input CSV      : {latest_csv.name}")
    print(f"Rows processed : {rows_processed}")
    print(f"Output Excel   : {output_filename}")
    print(f"Processed CSV  : {processed_file}")
    print("=" * 60)


# ============================================================
# START SCRIPT
# ============================================================

if __name__ == "__main__":
    main()