from flask import Flask, request, jsonify
from flask_cors import CORS
from upi_organizer import UPIDataProcessor
import pandas as pd
import os
from datetime import datetime
from csv_agent import query_transactions, generate_detailed_report

app = Flask(__name__)
# Update CORS configuration to explicitly allow localhost:3000
CORS(app, resources={
    r"/api/*": {
        "origins": ["http://localhost:3000"],
        "methods": ["GET", "POST"],
        "allow_headers": ["Content-Type"]
    }
})

processor = UPIDataProcessor()
user_upi_id = []
application_id = ''
if not os.path.exists('all_csvs'):
    os.makedirs('all_csvs')
@app.route('/api/accepttext', methods=['GET', 'POST'])
def set_upi():
    global user_upi_id
    
    if request.method == 'GET':
        if user_upi_id:
            return jsonify({"message": "UPI ID is set, adding one more", "upiId": user_upi_id}), 200
        return jsonify({"error": "UPI ID not set"}), 400
        
    # Existing POST logic
    data = request.get_json()
    user_upi_id = data.get('upiId')
    return jsonify({"message": "UPI ID set successfully", "upiId": user_upi_id}), 200

UPLOAD_FOLDER = "uploaded_files"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
@app.route('/api/submit-loan-application', methods=['POST'])
def submit_loan_application():
    try:
        # Basic form data
        form_data = {
            'loanPurpose': request.form.get('loanPurpose'),
            'incomeSource': request.form.get('incomeSource'),
            'useUpi': request.form.get('useUpi'),
            #'upiEntries': upi_entries
        }

        # Dynamic UPI entries handling
        upi_entries = []
        form_keys = request.form.keys()
        
        # Get the number of UPI entries from the form structure
        max_index = -1
        for key in form_keys:
            if key.startswith('upiEntries['):
                index = int(key.split('[')[1].split(']')[0])
                max_index = max(max_index, index)
        
        # Initialize entries
        for i in range(max_index + 1):
            entry = {
                'upiId': request.form.get(f'upiEntries[{i}][upiId]', ''),
                'isOwn': request.form.get(f'upiEntries[{i}][isOwn]', ''),
                'relationship': request.form.get(f'upiEntries[{i}][relationship]', ''),
                'frequency': request.form.get(f'upiEntries[{i}][frequency]', '')
            }
            upi_entries.append(entry)
            print(upi_entries)

        saved_files = []
        
        # Save UPI transaction files
        for i, entry in enumerate(upi_entries):
            file_key = f'upiEntries[{i}][transactionFile]'
            if file_key in request.files:
                file = request.files[file_key]
                filename = f"upi_transaction_{i}_{file.filename}"
                filepath = os.path.join(UPLOAD_FOLDER, filename)
                file.save(filepath)
                saved_files.append(filepath)

        # Save other files
        for file_key, folder_name in [('offlineRecords', 'offline_records'), 
                                    ('documents', 'identity_documents')]:
            if file_key in request.files:
                files = request.files.getlist(file_key)
                for file in files:
                    filename = f"{file.filename}"
                    filepath = os.path.join(UPLOAD_FOLDER, folder_name, filename)
                    os.makedirs(os.path.dirname(filepath), exist_ok=True)
                    file.save(filepath)
                    saved_files.append(filepath)

        # Save form data CSV
        # Save form data CSV
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        csv_file_path = os.path.join(UPLOAD_FOLDER, f"loan_application_{timestamp}.csv")

        # Create a dictionary with all form data including UPI entries
        csv_data = {
            **form_data,
            'files': saved_files,
            'upi_ids': [entry['upiId'] for entry in upi_entries],
            'is_own': [entry['isOwn'] for entry in upi_entries],
            'relationships': [entry['relationship'] for entry in upi_entries],
            'frequencies': [entry['frequency'] for entry in upi_entries]
        }

        pd.DataFrame([csv_data]).to_csv(csv_file_path, index=False)
        return jsonify({
            "message": "Application submitted successfully",
            "applicationId": timestamp,
            "savedFiles": saved_files
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/analyze', methods=['POST'])
def analyze_application():
    global application_id
    try:
        application_id = request.json.get('applicationId')
        csv_path = os.path.join(UPLOAD_FOLDER, f"loan_application_{application_id}.csv")
        
        application_data = pd.read_csv(csv_path)
        files = eval(application_data['files'][0])  # Convert string representation to list
        
        analysis_results = []
        for file_path in files:
            normalized_path = os.path.normpath(file_path)
            result = processor.process_document(normalized_path)
            analysis_results.append(result)
            
        return jsonify({
            "message": "Analysis completed",
            "results": analysis_results
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/query-transactions', methods=['POST'])
def analyze_transactions():
    try:
        question = request.json.get('question')
        result = query_transactions(question)
        return jsonify({
            "status": "success",
            "result": result
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/generate-report', methods=['GET'])
def get_transaction_report():
    try:
        report = generate_detailed_report()
        
        from csv_agent import convert_text_to_pdf_beautified
        
        convert_text_to_pdf_beautified(report, "report.pdf")
        
        return jsonify({
            "status": "success",
            "report": report
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500 

if __name__ == '__main__':
    app.run(debug=True, port=5000)