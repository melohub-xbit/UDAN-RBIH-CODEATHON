import pandas as pd
import re
import pdfplumber
from transformers import pipeline

# Step 1: Extract tabular data from PDF
def extract_tables_from_pdf(file_path):
    with pdfplumber.open(file_path) as pdf:
        tables = []
        for page in pdf.pages:
            for table in page.extract_tables():
                tables.append(pd.DataFrame(table))
                print(table)
        return tables

# Step 2: Process extracted tables to identify the relevant one
def process_extracted_tables(tables, possible_mappings):
    processed_tables = []
    for table in tables:
        # Set the first row as the header if the table has a header
        table.columns = table.iloc[0]
        table = table[1:]  # Drop the first row
        table = table.reset_index(drop=True)

        # Map columns dynamically
        table = map_columns(table, possible_mappings)

        # Check if the required columns exist in this table
        if all(col in table.columns for col in ['Date', 'Description', 'Amount']):
            processed_tables.append(table)
    return processed_tables

# Step 3: Map column names dynamically
def map_columns(dataframe, possible_mappings):
    column_map = {}
    for target_col, variations in possible_mappings.items():
        for col in dataframe.columns:
            if any(re.search(variation, str(col), re.IGNORECASE) for variation in variations):
                column_map[col] = target_col
                break
    return dataframe.rename(columns=column_map)

# Step 4: Extract UPI transactions
def extract_upi_transactions(data, description_column):
    upi_pattern = r'UPI|GooglePay|PhonePe|Paytm|BHIM|AmazonPay'
    return data[data[description_column].str.contains(upi_pattern, case=False, na=False)]

# Step 5: Categorize transactions using Hugging Face's zero-shot classification
def categorize_with_huggingface(descriptions):
    """
    Use Hugging Face's zero-shot classification to categorize transactions.
    :param descriptions: A list of transaction descriptions.
    :return: A list of categories assigned by the model.
    """
    # Load zero-shot classification pipeline
    classifier = pipeline("zero-shot-classification")

    # Define categories
    categories = ['Personal', 'Business', 'Miscellaneous']

    # Classify descriptions
    results = []
    for description in descriptions:
        result = classifier(description, candidate_labels=categories)
        results.append(result['labels'][0])  # Get the highest confidence label
    return results

# Step 6: Save the categorized data
def save_categorized_data(transactions, output_path):
    transactions.to_csv(output_path, index=False)

# Main execution
if __name__ == "__main__":
    file_path = "send.pdf"  # Replace with your file path
    output_path = "categorized_transactions.csv"
    possible_mappings = {
        'Date': ['date', 'transaction date'],
        'Description': ['description', 'details', 'narration'],
        'Amount': ['amount', 'transaction amount', 'debit', 'credit'],
        'Balance': ['balance', 'running balance']
    }

    # Step 1: Extract tables from PDF
    tables = extract_tables_from_pdf(file_path)

    # Step 2: Process tables to find the relevant transaction data
    processed_tables = process_extracted_tables(tables, possible_mappings)

    if processed_tables:
        for idx, table in enumerate(processed_tables):
            print(f"Processing table {idx + 1}...")
            # Step 3: Extract UPI transactions
            upi_transactions = extract_upi_transactions(table, 'Description')
            
            # Step 4: Categorize transactions using Hugging Face model
            descriptions = upi_transactions['Description'].tolist()
            categories_assigned = categorize_with_huggingface(descriptions)
            upi_transactions['Category'] = categories_assigned
            
            # Step 5: Save categorized transactions
            save_categorized_data(upi_transactions, output_path.replace('.csv', f'_{idx + 1}.csv'))
            print(f"Table {idx + 1} UPI transactions saved.")
    else:
        print("No valid tables found with the required columns.")
