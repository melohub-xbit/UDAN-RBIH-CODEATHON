import requests
import json
import os
import yaml
import csv
from datetime import datetime
from dataclasses import dataclass, asdict
from typing import Optional, Dict, List
from prompts import UPI_PARSER_PROMPT, TRANSACTION_ANALYSIS_PROMPT, MERCHANT_VERIFY_PROMPT

@dataclass
class UPIData:
    is_merchant: bool
    name: str
    bank: str
    confidence: float

@dataclass
class TransactionData:
    raw_transaction: str
    upi_id: str
    amount: float
    transaction_type: str
    recipient_type: str
    category: str
    bank: str
    recipient_name: str
    date: str
    merchant_info: Optional[Dict] = None

class TransactionAnalyzer:
    def __init__(self, model="llama3.2:3b", endpoint="http://localhost:11434/api/generate"):
        self.load_config()
        self.model = model
        self.endpoint = endpoint
        self.headers = {"Content-Type": "application/json"}
        self.serper_headers = {
            'X-API-KEY': os.environ['SERPER_DEV_API_KEY'],
            'Content-Type': 'application/json'
        }
        self.known_merchants = {}
        self.known_individuals = {}
        self.known_banks = {}
        self.output_file = f"transactions_updated.csv"

    def load_config(self, file_path='config.yaml'):
        with open(file_path, 'r') as file:
            config = yaml.safe_load(file)
            for key, value in config.items():
                os.environ[key] = value

    def _call_ollama(self, prompt: str, system_prompt: str, temperature: float = 0.8, max_retries: int = 3) -> dict:
        print(f"\n[DEBUG] Making Groq API call with prompt: {prompt[:100]}...")
        from groq import Groq
        from time import sleep
        
        client = Groq(api_key="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")
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ]
        
        for attempt in range(max_retries):
            try:
                completion = client.chat.completions.create(
                    model="llama-3.1-70b-versatile",  # Faster model
                    messages=messages,
                    temperature=temperature,
                    max_tokens=1024,  # Reduced for faster response
                    top_p=1,
                    stream=False,
                    stop=None
                )
                print(f"[DEBUG] Groq API call completed successfully on attempt {attempt + 1}")
                
                response = completion.choices[0].message.content
                parsed_response = json.loads(response)
                
                # Validate required fields
                required_fields = {'is_merchant', 'name', 'bank'}
                if not all(field in parsed_response for field in required_fields):
                    raise ValueError("Missing required fields in response")
                    
                if "confidence" not in parsed_response:
                    parsed_response["confidence"] = 1.0
                    
                print(f"[DEBUG] Parsed response: {parsed_response}")
                return parsed_response
                
            except (json.JSONDecodeError, ValueError) as e:
                print(f"[DEBUG] Attempt {attempt + 1} failed: {str(e)}")
                if attempt < max_retries - 1:
                    sleep(1)  # Brief delay between retries
                    continue
                
            except Exception as e:
                print(f"[DEBUG] Unexpected error on attempt {attempt + 1}: {str(e)}")
                if attempt < max_retries - 1:
                    sleep(1)
                    continue
        
        # Return default values after all retries exhausted
        print("[DEBUG] All retry attempts failed, returning default values")
        return {
            "is_merchant": False,
            "name": prompt,
            "bank": "unknown",
            "confidence": 0.0
        }

    def _search_merchant(self, merchant_name: str, upi_id: str) -> List[Dict]:
        print(f"\n[DEBUG] Performing web search for merchant: {merchant_name}")
        try:
            response = requests.post(
                "https://google.serper.dev/search",
                headers=self.serper_headers,
                json={"q": f"{merchant_name} business type"}
            )
            results = response.json().get('organic', [])
            print(f"[DEBUG] Found {len(results)} search results")
            return [{'title': r.get('title', ''), 'snippet': r.get('snippet', '')} 
                   for r in results[:2]]
        except Exception as e:
            print(f"[DEBUG] Search failed with error: {str(e)}")
            return [{"error": f"Search failed: {str(e)}"}]

    def get_standardized_name(self, upi_data: UPIData, merchant_info=None) -> str:
        name = upi_data.name.lower()
        if upi_data.is_merchant:
            if name in self.known_merchants:
                return self.known_merchants[name]
            if merchant_info:
                verified = self._call_ollama(
                    prompt=json.dumps({"name": name, "info": merchant_info}),
                    system_prompt=MERCHANT_VERIFY_PROMPT
                )
                try:
                    standardized = verified["verified_name"]
                except Exception as e:
                    print(f"[DEBUG] Error verifying merchant: {str(e)}")
                    standardized = name
                self.known_merchants[name] = standardized
                return standardized
            return name
        else:
            if name in self.known_individuals:
                return self.known_individuals[name]
            self.known_individuals[name] = name
            return name

    def get_bank_name(self, upi_id: str) -> str:
        if upi_id in self.known_banks:
            return self.known_banks[upi_id]
        bank_name = self.parse_upi_id(upi_id).bank
        self.known_banks[upi_id] = bank_name
        return bank_name

    def parse_upi_id(self, upi_id: str) -> UPIData:
        if upi_id in self.known_banks:
            bank = self.known_banks[upi_id]
            parsed = self._call_ollama(prompt=upi_id, system_prompt=UPI_PARSER_PROMPT)
            parsed['bank'] = bank
            return UPIData(**parsed)
        parsed = self._call_ollama(prompt=upi_id, system_prompt=UPI_PARSER_PROMPT)
        self.known_banks[upi_id] = parsed['bank']
        return UPIData(**parsed)

    def save_transaction(self, transaction_data: TransactionData):
        exists = os.path.exists(self.output_file)

    def analyze_transaction(self, transaction: str) -> TransactionData:
        print(f"\n[DEBUG] Starting analysis for transaction: {transaction}")
        date_str = transaction.split()[0]
        upi_id = transaction.split('@')[0] + '@' + transaction.split('@')[1].split()[0]
        print(f"[DEBUG] Extracted UPI ID: {upi_id}")
        
        upi_data = self.parse_upi_id(upi_id)
        print(f"[DEBUG] Parsed UPI data: {upi_data}")
        
        merchant_info = None
        if upi_data.is_merchant:
            print("[DEBUG] Merchant detected, performing web search")
            merchant_info = self._search_merchant(upi_data.name, upi_id)
        
        recipient_name = self.get_standardized_name(upi_data, merchant_info)
        print(f"[DEBUG] Standardized recipient name: {recipient_name}")
        
        print("[DEBUG] Performing transaction analysis with Groq")
        analysis = self._call_ollama(
            prompt=json.dumps({
                "transaction": transaction,
                "upi_data": asdict(upi_data),
                "merchant_info": merchant_info
            }),
            system_prompt=TRANSACTION_ANALYSIS_PROMPT
        )
        
        amount = abs(float(analysis["amount"]))
        if analysis["transaction_type"] == "debit" or "debited" in transaction.lower():
            amount = -amount
        print(f"[DEBUG] Final amount calculated: {amount}")
        
        transaction_data = TransactionData(
            raw_transaction=transaction,
            upi_id=upi_id,
            amount=amount,
            date=date_str,
            transaction_type=analysis["transaction_type"],
            recipient_type=analysis["recipient_type"],
            category=analysis["category"],
            bank=upi_data.bank,
            recipient_name=recipient_name,
            merchant_info=merchant_info
        )
        
        print("[DEBUG] Saving transaction to CSV")
        self.save_transaction(transaction_data)
        print("[DEBUG] Transaction analysis completed")
        with open(self.output_file, 'a', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=asdict(transaction_data).keys())
            if not writer.writeheader():
                writer.writerow(asdict(transaction_data))
        return transaction_data
    

    def analyze_transaction(self, transaction: str) -> TransactionData:
        date_str = transaction.split()[0]
        upi_id = transaction.split('@')[0] + '@' + transaction.split('@')[1].split()[0]
        
        upi_data = self.parse_upi_id(upi_id)
        
        merchant_info = None
        if upi_data.is_merchant:
            merchant_info = self._search_merchant(upi_data.name, upi_id)
        
        recipient_name = self.get_standardized_name(upi_data, merchant_info)
        
        analysis = self._call_ollama(
            prompt=json.dumps({
                "transaction": transaction,
                "upi_data": asdict(upi_data),
                "merchant_info": merchant_info
            }),
            system_prompt=TRANSACTION_ANALYSIS_PROMPT
        )
        
        # Take absolute value of amount and set sign based on transaction type
        amount = abs(float(analysis["amount"]))
        if analysis["transaction_type"] == "debit" or "debited" in transaction.lower():
            amount = -amount
        
        transaction_data = TransactionData(
            raw_transaction=transaction,
            upi_id=upi_id,
            amount=amount,
            date=date_str,
            transaction_type=analysis["transaction_type"],
            recipient_type=analysis["recipient_type"],
            category=analysis["category"],
            bank=upi_data.bank,
            recipient_name=recipient_name,
            merchant_info=merchant_info
        )
        
        self.save_transaction(transaction_data)
        return transaction_data

    def batch_process(self, transactions: List[str]) -> List[TransactionData]:
        return [self.analyze_transaction(tx) for tx in transactions]

def main():
    analyzer = TransactionAnalyzer()
    
    transactions = [
        "INR 500 debited to swiggy.75839@okicici",
        "INR 1000 credited from yash.gupta123@hdfc",
        "INR 200 debited to 9876543210@paytm",
        "INR 799 debited to netflix.sub12@okaxis"
    ]
    
    results = analyzer.batch_process(transactions)
    
    for result in results:
        print(f"\nTransaction: {result.raw_transaction}")
        print(f"UPI ID: {result.upi_id}")
        print(f"Amount: {result.amount}")
        print(f"Category: {result.category}")
        print(f"Type: {result.transaction_type}")
        print(f"Recipient: {result.recipient_name}")
        print(f"Bank: {result.bank}")

if __name__ == "__main__":
    main()