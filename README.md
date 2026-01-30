🏠 Land Registry Data Automation Suite

A robust two-stage Python pipeline designed to automate the enrichment and validation of property listing data using official UK Government Land Registry records.
🎯 Project Overview

This tool eliminates manual data entry by programmatically fetching transaction details from the Land Registry SPARQL endpoint. It ensures data integrity by cross-referencing internal listing dates with official government sale records, providing an automated "source of truth" for FP&A and property teams.
🔄 How the Pipeline Works

The system is split into two modular phases to ensure scalability and easy error tracking:
1. Enrichment Phase (scripts/land_registry_lookup.py)

    Input: Takes a raw lead list from data/Input Data.xlsx.

    Process:

        Normalizes postcodes into standard UK formats.

        Executes real-time SPARQL queries against the Land Registry database to find the latest "Price Paid" data.

    Output: Generates a check file with official matched addresses, sold values, and sale dates.

2. Processing & Validation Phase (scripts/land-registry-data-processor.py)

    Input: The enriched data from Phase 1.

    Logical Validation: Performs a critical chronological check to ensure the sold_date is on or after the first_instructed_date.

    Database Upsert: Merges validated data into the master file (Final_Data_2025.xlsx), intelligently updating existing records by property_id while appending new entries.

📁 Repository Structure

Organized for clarity and professional standards:

    /scripts: Contains the Python logic for API handling and data merging.

    /data: Contains sample datasets and the final master record.

    requirements.txt: Lists all necessary dependencies for easy setup.

    .gitignore: Configured to prevent local Excel artifacts from being tracked.

🛠️ Tech Stack

    Python 3.x

    Pandas: For high-performance data manipulation.

    Requests & SPARQL: For interacting with Linked Data endpoints.

    OpenPyXL: For Excel file management.
