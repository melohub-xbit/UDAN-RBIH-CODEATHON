UPI_PARSER_PROMPT = """Analyze this UPI ID and extract structured information.
Common patterns include:
- (person_name)(number)@bank
- (person_name).(number)@bank  
- (phonenumber)@bank
- (business_name)(identifier)@bank

bank name can be one of these hdfc, icici, sbi, axis, paytm, okicici, okhdfc, oksbi, okaxis
Return in this exact JSON format using only ASCII characters:
{
    "is_merchant": true/false,
    "name": "extracted name in lowercase ASCII only",
    "bank": "bank name",
    "confidence": 0.0-1.0
}"""

TRANSACTION_ANALYSIS_PROMPT = """Analyze this UPI transaction.
Use only ASCII characters in the response.
For amounts, use numbers only without currency symbols.

Return in this exact JSON format:
{
    "category": "food/transport/entertainment/utilities/shopping/health/education/other",
    "transaction_type": "credit/debit", 
    "amount": 0.00,
    "is_business_transaction": true/false,
    "recipient_type": "merchant/individual"
}"""

MERCHANT_VERIFY_PROMPT = """Extract the actual business name from search results.
Example: For "swiggy.75839@okicici", return "swiggy"
For "netflix.sub12@okaxis", return "netflix"

Return in this exact JSON format:
{
    "verified_name": "actual business name in lowercase ASCII"
}"""
