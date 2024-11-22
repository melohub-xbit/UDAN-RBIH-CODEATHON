import pandas as pd
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
import os
import google.generativeai as genai

def create_analysis_pdf(analysis_text, output_pdf_path="analysis_report.pdf"):
    """Convert Gemini's analysis into a well-formatted PDF"""
    doc = SimpleDocTemplate(output_pdf_path, pagesize=letter)
    styles = getSampleStyleSheet()
    
    # Create custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        spaceAfter=30
    )
    
    section_style = ParagraphStyle(
        'SectionHeader',
        parent=styles['Heading2'],
        fontSize=16,
        spaceAfter=12,
        spaceBefore=20
    )
    
    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['Normal'],
        fontSize=12,
        leading=14,
        spaceAfter=8
    )
    
    # Build the PDF content
    elements = []
    
    # Add title
    elements.append(Paragraph("Transaction Analysis Report", title_style))
    elements.append(Spacer(1, 20))
    
    # Process and add analysis sections
    sections = analysis_text.split('\n\n')
    for section in sections:
        if section.strip():
            if section.isupper() or section.endswith(':'):
                # Treat as section header
                elements.append(Paragraph(section, section_style))
            else:
                # Regular content
                elements.append(Paragraph(section, body_style))
            elements.append(Spacer(1, 10))
    
    # Generate PDF
    doc.build(elements)

def create_pdf_from_csv(csv_path, output_pdf_path):
    """Convert CSV to a formatted PDF"""
    df = pd.read_csv(csv_path)
    
    doc = SimpleDocTemplate(output_pdf_path, pagesize=letter)
    elements = []
    
    # Convert DataFrame to list of lists for the table
    table_data = [df.columns.tolist()] + df.values.tolist()
    table = Table(table_data)
    
    # Add style to the table
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    elements.append(table)
    doc.build(elements)

def analyze_multiple_csvs_with_gemini(csv_paths, model):
    """Analyze multiple CSVs using Gemini"""
    pdfs = []
    
    # Convert each CSV to PDF
    for csv_path in csv_paths:
        pdf_path = csv_path.replace('.csv', '.pdf')
        create_pdf_from_csv(csv_path, pdf_path)
        pdfs.append(pdf_path)
    
    # Upload PDFs to Gemini
    uploaded_files = [genai.upload_file(pdf, mime_type="application/pdf") for pdf in pdfs]
    
    # Create analysis prompt
    analysis_prompt = """Analyze these transaction records and provide a detailed financial behavior summary under these headers:

    1. INCOME PATTERNS
    - Frequency and consistency of credits
    - Primary income sources
    - Average monthly inflows
    - Additional income streams
    
    2. SPENDING BEHAVIOR
    - Essential expenses (rent, utilities, groceries)
    - Discretionary spending patterns
    - Major recurring payments
    - Category-wise expenditure breakdown
    
    3. FINANCIAL MANAGEMENT
    - Cash flow patterns
    - Balance maintenance trends
    - Savings indicators
    - Investment activities
    
    4. TRANSACTION RELIABILITY
    - Payment consistency
    - Transaction success rate
    - Regular bill payments
    - EMI/recurring payment history
    
    5. OVERALL FINANCIAL PROFILE
    - Key strengths in financial behavior
    - Areas needing attention
    - Month-on-month stability
    - Notable financial patterns

    Present factual data with specific numbers and percentages under each section.
    Focus on objective transaction patterns without making lending recommendations."""

    # Start chat session with all files
    chat_session = model.start_chat(
        history=[{
            "role": "user",
            "parts": uploaded_files + [analysis_prompt]
        }]
    )
    
    # Get analysis
    response = chat_session.send_message("Please analyze these transaction records as described.")
    
    return response.text


def main():
    # Configure Gemini
    generation_config = {
        "temperature": 0.7,
        "top_p": 0.9,
        "top_k": 40,
        "max_output_tokens": 8192,
    }
    
    model = genai.GenerativeModel(
        model_name="gemini-1.5-pro-002",
        generation_config=generation_config
    )
    
    # Get all CSV files in directory
    csv_files = [f for f in os.listdir('.') if f.endswith('_transactions.csv')]
    
    # Analyze CSVs
    analysis = analyze_multiple_csvs_with_gemini(csv_files, model)
    create_analysis_pdf(analysis, "transaction_analysis_report.pdf")    
    
    print("Analysis complete! Check transaction_analysis_report.txt for results.")

if __name__ == "__main__":
    main()
