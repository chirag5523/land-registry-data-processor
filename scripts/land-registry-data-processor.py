import pandas as pd
import os

def process_land_registry_data():
    """
    Process land registry data by filtering matched records,
    formatting dates, adding Checks column, and updating Final Data 2024.xlsx
    """

    # File paths
    base_path = r"C:\Users\Chirag.Lalitcumar\Land Registry Data"
    source_file = os.path.join(base_path, "Output_Land_Registery_Check_2025.xlsx")
    target_file = os.path.join(base_path, "Final_Data_2025.xlsx")

    # Columns to keep
    required_columns = [
        "property_id", "postcode", "address_display", "property_status", "payment_plan",
        "first_instructed_date", "first_listed_date", "house_number_final", "road_final",
        "address_clean", "matched_address", "sold_value", "sold_date", "category", "status"
    ]

    try:
        print("Starting data processing...")

        if not os.path.exists(source_file):
            print(f"Error: Source file not found: {source_file}")
            return

        print("Reading source file...")
        source_df = pd.read_excel(source_file, sheet_name='Sheet1')

        # Filter matched records
        matched_records = source_df[source_df['status'].str.contains('matched', case=False, na=False)]
        matched_records = matched_records[required_columns]

        if matched_records.empty:
            print("No matched records found. Nothing to process.")
            return

        # Re-convert for comparison (need datetime objects for >= check)
        matched_records["first_instructed_date_dt"] = pd.to_datetime(matched_records["first_instructed_date"], format="%d/%m/%Y", errors="coerce")
        matched_records["sold_date_dt"] = pd.to_datetime(matched_records["sold_date"], format="%d/%m/%Y", errors="coerce")

        # Add Checks column
        matched_records["Checks"] = matched_records["sold_date_dt"] >= matched_records["first_instructed_date_dt"]

        # Drop helper columns
        matched_records = matched_records.drop(columns=["first_instructed_date_dt", "sold_date_dt"])

        # Check if target file exists
        if os.path.exists(target_file):
            target_df = pd.read_excel(target_file, sheet_name='Sheet1')
            target_df = target_df[required_columns + ["Checks"]] if "Checks" in target_df.columns else target_df[required_columns]
        else:
            target_df = pd.DataFrame(columns=required_columns + ["Checks"])

        # Merge new data
        for _, row in matched_records.iterrows():
            property_id = row["property_id"]
            existing_mask = target_df["property_id"] == property_id

            if existing_mask.any():
                target_df.loc[existing_mask, :] = row.values
            else:
                target_df = pd.concat([target_df, row.to_frame().T], ignore_index=True)

        # Save output
        target_df.to_excel(target_file, sheet_name='Sheet1', index=False)
        print("Processing completed successfully!")

    except Exception as e:
        print(f"Unexpected error: {e}")

def main():
    print("Land Registry Data Processor")
    print("=" * 40)
    process_land_registry_data()

if __name__ == "__main__":
    main()
