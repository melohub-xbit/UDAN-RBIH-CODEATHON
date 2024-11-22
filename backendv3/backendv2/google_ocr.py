import os
import time
import google.generativeai as genai
from typing import Dict, List

def process_document_with_gemini(file_path: str) -> List[Dict]:
    """Process document using Gemini Vision API and return structured UPI transaction data"""
    
    genai.configure(api_key="AIzaSyB-Lghd5AdWpBeApKSFPZbqXh-TuYF3OQg")

    generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 40,
        "max_output_tokens": 8192,
    }

    model = genai.GenerativeModel(
        model_name="gemini-1.5-pro-002",
        generation_config=generation_config
    )

    # Upload and process file
    file = genai.upload_file(file_path)
    
    prompt = """Extract all UPI transaction data from this document and format as CSV with these columns:
    raw_transaction,upi_id,amount,transaction_type,recipient_type,category,bank,recipient_name,date
    
    Example format:
    2024-01-20 INR 500 debited to swiggy.75839@okicici for dinner,swiggy.75839@okicici,-500.0,debit,merchant,food,okicici,swiggy,2024-01-20
    
    Rules for extraction:
    - For merchants: Extract business name from UPI ID
    - For individuals: Use name from transaction details
    - Categories: food/transport/entertainment/utilities/shopping/health/education/other
    - Transaction type: credit/debit
    - Recipient type: merchant/individual
    - Amount should be negative for debits, positive for credits
    - Use only ASCII characters
    """

    response = model.generate_content([prompt, file])
    
    # Parse CSV response into list of dictionaries
    transactions = []
    csv_lines = response.text.strip().split('\n')
    headers = csv_lines[0].split(',')
    
    for line in csv_lines[1:]:
        values = line.split(',')
        transaction = dict(zip(headers, values))
        transactions.append(transaction)
    print(transactions)
    return transactions
process_document_with_gemini('./uploaded_files/upi_transaction_0_testing.pdf')
