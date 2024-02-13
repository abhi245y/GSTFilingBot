import os
import pandas as pd

def aggregate_duplicate_hsn(df):
    # Group the DataFrame by 'HSN' and sum the values of other columns
    aggregated_df = df.groupby('HSN').agg({
        'Description': 'first',  # Take the first description (assuming it's the same for duplicates)
        'UQC': 'first',          # Take the first UQC (assuming it's the same for duplicates)
        'Total Quantity': 'sum',
        'Total Value': 'sum',
        'Rate': 'mean',           # Take the mean rate (assuming it's the same for duplicates)
        'Taxable Value': 'sum',
        'Integrated Tax Amount': 'sum',
        'Central Tax Amount': 'sum',
        'State/UT Tax Amount': 'sum',
        'Cess Amount': 'sum'
    }).reset_index()  # Reset the index to move 'HSN' back to a column

    return aggregated_df

def read_excel_and_aggregate(file_path):
    try:
        # Read the Excel file into a pandas DataFrame
        df = pd.read_excel(file_path, dtype={'HSN': str})

        # Print the DataFrame after reading
        print(f"DataFrame for file: {file_path}")
        print(df)
        print()

        if df.empty:
            print("No records in the DataFrame.")
            return df

        # Aggregate duplicate HSN entries
        aggregated_df = aggregate_duplicate_hsn(df)

        # Print the aggregated DataFrame
        print("Aggregated DataFrame:")
        print(aggregated_df)
        print()

        # Write aggregated_df to Excel file
        result_file_path = os.path.join(os.path.dirname(file_path), 'result.xlsx')
        aggregated_df.to_excel(result_file_path, index=False)
        print(f"Aggregated DataFrame saved to: {result_file_path}")

        return aggregated_df

    except PermissionError:
        print(f"PermissionError: Could not read file: {file_path}. Skipping...")
        return pd.DataFrame()

def read_and_aggregate_all_excel_sheets_in_directory():
    # Get the directory of the Python file
    current_directory = os.path.dirname(os.path.abspath(__file__))

    # Get all Excel files in the directory
    excel_files = [file for file in os.listdir(current_directory) if file.endswith('.xlsx')]

    # Iterate through each Excel file and perform aggregation
    for file in excel_files:
        file_path = os.path.join(current_directory, file)
        print(f"Reading and aggregating file: {file}")
        read_excel_and_aggregate(file_path)
        print()

# Example usage:
if __name__ == "__main__":
    read_and_aggregate_all_excel_sheets_in_directory()
