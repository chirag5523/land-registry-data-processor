# 🏠 Land Registry Data Processor

An automation tool designed to streamline the processing of UK Land Registry records. This script handles data ingestion, logical validation of transaction dates, and incremental updates to a master database.

## 🚀 Key Features
* **Automated Filtering:** Isolates "matched" records instantly.
* **Date Validation:** Ensures `sold_date` is chronologically after `first_instructed_date`.
* **Smart Merge (Upsert):** Updates existing property records by ID or appends new ones, preventing duplicates.
* **Excel Integration:** Seamlessly reads and writes to `.xlsx` formats.

## 🛠️ Tech Stack
* **Language:** Python 3.x
* **Libraries:** Pandas (Data manipulation), OpenPyXL (Excel engine)

## 📋 How to Use
1. Clone the repository.
2. Install dependencies: `pip install -r requirements.txt`
3. Update the `base_path` in the script to your local directory.
4. Run the script
