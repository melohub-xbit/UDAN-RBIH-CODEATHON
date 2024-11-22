import os
import traceback
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
import dotenv
import csv
from datetime import datetime


dotenv.load_dotenv()
def diagnose_gemini_api_issues(file_path):
    """
    Comprehensive diagnostic function for Gemini API issues
    """
    try:
        # 1. Verify API Key
        api_key = os.getenv('GOOGLE_AI_API_KEY')
        if not api_key:
            print("❌ ERROR: No API key found. Set GOOGLE_AI_API_KEY environment variable.")
            return False

        # 2. Check library version
        print(f"📦 Generative AI Library Version: {genai.__version__}")

        # 3. Configure with additional safety settings
        genai.configure(
            api_key=api_key,
            transport='rest'  # Use REST transport instead of gRPC
        )

        # 4. Detailed logging and error handling
        safety_settings = {
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
        }

        # 5. File validation
        if not os.path.exists(file_path):
            print(f"❌ ERROR: File not found at {file_path}")
            return False

        # 6. Verbose file upload
        print("📤 Uploading file...")
        try:
            file = genai.upload_file(file_path)
            print(f"✅ File uploaded successfully: {file.name}")
        except Exception as upload_error:
            print(f"❌ File upload error: {upload_error}")
            traceback.print_exc()
            return False

        # 7. Model initialization with extensive configuration
        generation_config = {
            "temperature": 0.5,
            "top_p": 0.9,
            "max_output_tokens": 2048,
        }

        model = genai.GenerativeModel(
            model_name="gemini-1.5-pro-002",
            generation_config=generation_config,
            safety_settings=safety_settings
        )

        # 8. Detailed prompt with error handling
        prompt = """Strictly process this document and extract UPI transactions.
        Respond in clean, well-formatted CSV without any extra markers or code block delimiters.
        If no transactions found, return an empty CSV with headers."""

        print("🚀 Generating content...")
        try:
            response = model.generate_content([prompt, file])
            #save response to a csv file
            # Generate timestamp for unique filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            csv_filename = f'./extracted_transactions_{timestamp}.csv'
            
            # Write response to CSV file
            with open(csv_filename, 'w', newline='') as csvfile:
                csvfile.write(response.text)
    
            print(f"\n💾 Response saved to: {csv_filename}")
            
            print("\n📄 Response Received:")
            print(response.text)
            return True
        
        except Exception as gen_error:
            print(f"❌ Content generation error: {gen_error}")
            traceback.print_exc()
            return False

    except Exception as e:
        print(f"🔥 Unexpected error: {e}")
        traceback.print_exc()
        return False

# Diagnostic run
result = diagnose_gemini_api_issues('./uploaded_files/upi_transaction_0_testing.pdf')
print("\n🔍 Diagnostic Result:", "PASSED" if result else "FAILED")