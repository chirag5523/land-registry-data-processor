# 🏠 Land Registry Data Processor

This project is a two-stage Python automation pipeline designed to validate property listing data against official UK Land Registry records. It handles everything from API data retrieval to logical validation and incremental database updates.

🔄 Project Workflow
graph TD
    A[Input Data.xlsx] --> B(land_registry_lookup.py)
    B -->|API Query| C[Land Registry SPARQL Endpoint]
    C --> B
    B --> D[Output_Land_Registery_Check.xlsx]
    D --> E(land-registry-data-processor.py)
    E -->|Validation & Merge| F[(Final_Data_2025.xlsx)]

The system operates in two distinct phases:
Phase 1: Data Enrichment (land_registry_lookup.py)

This script acts as the data ingestion engine.

    Input: A raw Excel file (Input Data.xlsx) containing internal property leads.

    Process: It iterates through each record, normalizes the postcode, and queries the Official Land Registry SPARQL Endpoint.

    Output: Generates Output_Land_Registery_Check.xlsx. This file contains the official "Price Paid" data, transaction dates, and a "matched" status for every property.

Phase 2: Logical Validation & Merging (land-registry-data-processor.py)

This script serves as the business logic and database manager.

    Input: The enriched file generated in Phase 1 (Output_Land_Registery_Check.xlsx).

    Process: * Filters for "matched" records.

        Date Integrity Check: Validates that the sold_date (from Land Registry) is chronologically after the first_instructed_date (internal data).

        Smart Update (Upsert): Compares records against the master file (Final_Data_2025.xlsx). It updates existing records based on property_id or appends new unique entries.

    Output: A clean, updated master Excel database ready for FP&A reporting.
## 🚀 Key Features
* **Automated Filtering:** Isolates "matched" records instantly.
* **Date Validation:** Ensures `sold_date` is chronologically after `first_instructed_date`.
* **Smart Merge (Upsert):** Updates existing property records by ID or appends new ones, preventing duplicates.
* **Excel Integration:** Seamlessly reads and writes to `.xlsx` formats.

## 🛠️ Tech Stack
* **Language:** Python 3.x
* **Libraries:** Pandas (Data manipulation), OpenPyXL (Excel engine)

🛠️ Installation & Setup

    Clone the repository:
    Bash

    git clone https://github.com/your-username/your-repo-name.git

    Install Dependencies:
    Bash

    pip install pandas openpyxl requests urllib3

    Prepare Data: Ensure your Input Data.xlsx is in the same directory as the scripts.

📊 Data Structure

The system expects the following key columns in the input data:

    property_id, postcode, door_number, first_instructed_date, and property_status.

🚀 Key Features

    SPARQL Query Integration: Directly interfaces with UK Government Linked Data.

    Error Handling: Built-in retry logic and API request throttling to ensure stable data retrieval.

    Automated Upsert: Prevents data duplication in the master record.

    Date Validation: Ensures high data quality by catching illogical transaction timelines.
