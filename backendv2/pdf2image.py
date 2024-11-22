import os
import time
import google.generativeai as genai

# Configure API Key
genai.configure(api_key=os.environ["API_KEY"])

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

# Define model and configuration
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-pro",
    generation_config=generation_config,
    system_instruction=(
        "Given an image/document of a bank statement, bills, etc., return a CSV-formatted string. "
        "The CSV format has the following headers: raw_transaction, upi_id, amount, transaction_type, "
        "recepient_type, category, bank, recepient_name"
    ),
)

def clean_csv_content(csv_content):
    """
    Cleans the CSV content by removing the ```csv``` markers.
    """
    # Strip the ```csv``` markers if present
    return csv_content.strip("```csv").strip("```").strip()

def save_csv(content, output_path):
    """Saves a cleaned CSV-formatted string to a CSV file."""
    cleaned_content = clean_csv_content(content)
    with open(output_path, mode="w", newline="") as csv_file:
        csv_file.write(cleaned_content)
    print(f"CSV saved to {output_path}")

# Main script
def process_pdf_with_gemini(pdf_path, output_csv_path):
    """Uploads a PDF to Gemini, processes it, and saves the cleaned CSV output."""
    # Upload the PDF
    files = [upload_to_gemini(pdf_path, mime_type="application/pdf")]

    # Wait for files to be processed
    wait_for_files_active(files)

    # Start chat session and send the message
    chat_session = model.start_chat(
        history=[
            {
                "role": "user",
                "parts": [files[0]],
            }
        ]
    )

    # Send the request and process the response
    response = chat_session.send_message("Please process this document as described.")
    csv_content = response.text

    # Save the cleaned response to a CSV file
    save_csv(csv_content, output_csv_path)

# Example usage
if __name__ == "__main__":
    pdf_path = "testing.pdf"  # Replace with your PDF file path
    output_csv_path = "output.csv"  # Replace with your desired CSV output path

    try:
        process_pdf_with_gemini(pdf_path, output_csv_path)
    except Exception as e:
        print(f"Error: {e}")
