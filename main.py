import os
import pandas as pd

def check_excel_sheet(file_path):
    try:
        # Read the Excel file into a pandas DataFrame
        df = pd.read_excel(file_path, dtype={'HSN': str,'Description': str})

        # Print the DataFrame after reading and dropping NaN values
        print(f"DataFrame for file: {file_path}")
        print(df)
        print()
        
        result_file_path = os.path.join(os.path.dirname(file_path), 'entry.xlsx')
        df.to_excel(result_file_path, index=False)
        print(f"Read saved to: {result_file_path}")

        if df.empty:
            print("No valid records after dropping NaN values.")
            return df

        valid_rows = []

        for index, row in df.iterrows():
            # Check condition 1: HSN field should have 4, 6, or 8 digits
            condition_1 = len(str(row['HSN'])) in [4, 6, 8]

            # Check condition 2: Central Tax Amount and State/UT Tax Amount should be equal to Taxable Value * (Rate/200) within a tolerance of plus or minus 0.02
            expected_value = row['Taxable Value'] * (row['Rate'] / 200)
            tolerance = 0.05
            condition_2 = abs(row['Central Tax Amount'] - row['State/UT Tax Amount']) <= tolerance and \
                          abs(row['Central Tax Amount'] - expected_value) <= tolerance

            # Check condition 3: Total Value should be the sum of Taxable Value, Integrated Tax Amount, Central Tax Amount, and State/UT Tax Amount
            tolerance = 0.01
            expected_total_value = row['Taxable Value'] + row['Integrated Tax Amount'] + row['Central Tax Amount'] + row['State/UT Tax Amount']
            condition_3 = abs(row['Total Value'] - expected_total_value) <= tolerance

            if condition_1 and condition_2 and condition_3:
                valid_rows.append(row)

                # # Print the valid row
                # print("Valid Record:")
                # print(row)
                # print()

        if not valid_rows:
            print("No valid records found.")
        else:
            # Convert valid_rows to DataFrame
            valid_records = pd.DataFrame(valid_rows)
            # Write valid_records to Excel file
            result_file_path = os.path.join(os.path.dirname(file_path), 'result.xlsx')
            valid_records.to_excel(result_file_path, index=False)
            print(f"Valid records saved to: {result_file_path}")

        return valid_records

    except PermissionError:
        print(f"PermissionError: Could not read file: {file_path}. Skipping...")
        return pd.DataFrame()

def check_all_excel_sheets_in_directory():
    # Get the directory of the Python file
    current_directory = os.path.dirname(os.path.abspath(__file__))

    # Get all Excel files in the directory
    excel_files = [file for file in os.listdir(current_directory) if file.endswith('.xlsx')]

    # Iterate through each Excel file and perform checks
    for file in excel_files:
        file_path = os.path.join(current_directory, file)
        print(f"Checking file: {file}")
        valid_records = check_excel_sheet(file_path)
        print(valid_records)
        print()

# Example usage:
if __name__ == "__main__":
    check_all_excel_sheets_in_directory()
