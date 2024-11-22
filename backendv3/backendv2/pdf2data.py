import os
import time
import google.generativeai as genai
import yaml

def load_config(file_path='config.yaml'):
    with open(file_path, 'r') as file:
        config = yaml.safe_load(file)
        for key, value in config.items():
            os.environ[key] = value

load_config()
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

def upload_to_gemini(path, mime_type=None):
    """Uploads the given file to Gemini."""
    file = genai.upload_file(path, mime_type=mime_type)
    print(f"Uploaded file '{file.display_name}' as: {file.uri}")
    return file

def wait_for_files_active(files):
    """Waits for the given files to be active."""
    print("Waiting for file processing...")
    for name in (file.name for file in files):
        file = genai.get_file(name)
        while file.state.name == "PROCESSING":
            print(".", end="", flush=True)
            time.sleep(10)
            file = genai.get_file(name)
        if file.state.name != "ACTIVE":
            raise Exception(f"File {file.name} failed to process")
    print("...all files ready")
    print()

generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}


model = genai.GenerativeModel(
    model_name="gemini-1.5-pro-002",
    generation_config=generation_config,
    system_instruction=(
        "Analyze bank statements and transaction documents to extract structured data.\n\n"
        "For UPI IDs, identify patterns like:\n"
        "- (person_name)(number)@bank\n"
        "- (person_name).(number)@bank\n"
        "- (phonenumber)@bank\n"
        "- (business_name)(identifier)@bank\n\n"
        "Bank names should be one of: hdfc, icici, sbi, axis, paytm, okicici, okhdfc, oksbi, okaxis\n\n"
        "Return a CSV-formatted string with these headers:\n"
        "raw_transaction, upi_id, amount, transaction_type, recepient_type, category, bank, recepient_name\n\n"
        "Where:\n"
        "- category: food/transport/entertainment/utilities/shopping/health/education/other\n"
        "- transaction_type: credit/debit\n"
        "- recepient_type: merchant/individual\n"
        "- amount: numeric value (positive for credit, negative for debit)\n"
        "Use only ASCII characters in all outputs."
        "If you don't find any data, return an NA fields."
    ),
)


def clean_csv_content(csv_content):
    """Cleans the CSV content by removing the ```csv``` markers."""
    return csv_content.strip("```csv").strip("```").strip()

def save_csv(content, output_path):
    """Saves a cleaned CSV-formatted string to a CSV file."""
    cleaned_content = clean_csv_content(content)
    with open(output_path, mode="w", newline="") as csv_file:
        csv_file.write(cleaned_content)
    print(f"CSV saved to {output_path}")

def process_document_with_gemini(file_path, output_csv_path):
    """Processes any supported document and returns structured transaction data."""
    print(f"[DEBUG] Processing file: {file_path}")
    
    # Upload file with appropriate mime type
    ext = os.path.splitext(file_path)[1].lower()
    mime_type = {
        '.pdf': 'application/pdf',
        '.txt': 'text/plain',
        '.png': 'image/png',
        '.jpg': 'image/jpeg',
        '.jpeg': 'image/jpeg'
    }.get(ext, 'application/octet-stream')
    
    files = [upload_to_gemini(file_path, mime_type=mime_type)]
    wait_for_files_active(files)

    chat_session = model.start_chat(
        history=[
            {
                "role": "user",
                "parts": [files[0]],
            }
        ]
    )

    response = chat_session.send_message("Please process this document as described.")
    csv_content = response.text
    save_csv(csv_content, output_csv_path)

    transactions = []
    csv_lines = clean_csv_content(csv_content).strip().split('\n')
    headers = csv_lines[0].split(',')
    
    for line in csv_lines[1:]:
        values = line.split(',')
        transaction = dict(zip(headers, values))
        transactions.append(transaction)
    
    print(f"[DEBUG] Extracted {len(transactions)} transactions")
    return transactions

if __name__ == "__main__":
    file_path = "./testing.pdf"
    if not os.path.exists("./all_csvs"):
        os.mkdir("./all_csvs")
    output_csv_path = "./all_csvs/output.csv"

    try:
        process_document_with_gemini(file_path, output_csv_path)
    except Exception as e:
        print(f"Error: {e}")
