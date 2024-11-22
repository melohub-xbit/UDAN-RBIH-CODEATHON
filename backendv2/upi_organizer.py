import pandas as pd
from datetime import datetime
from typing import List, Dict, Union
from search import TransactionAnalyzer
from dataclasses import asdict
import json
import os
from groq import Groq
if not os.path.exists('./all_csvs'):
            os.makedirs('./all_csvs')
class UPIDataProcessor:
    def __init__(self):
        self.transaction_analyzer = TransactionAnalyzer()

    def process_text_transactions(self, transactions: List[str]) -> pd.DataFrame:
        results = []
        for tx in transactions:
            analyzed = self.transaction_analyzer.analyze_transaction(tx)
            results.append(asdict(analyzed))
        return pd.DataFrame(results)

    def generate_insights(self, df: pd.DataFrame) -> Dict:
        insights = {
            'total_transactions': int(len(df)),
            'total_amount': float(df['amount'].sum()),
            'avg_transaction': float(df['amount'].mean()),
            'category_distribution': df['category'].value_counts().to_dict(),
            'merchant_distribution': df[df['recipient_type'] == 'merchant']['recipient_name'].value_counts().to_dict(),
            'bank_distribution': df['bank'].value_counts().to_dict()
        }
        return {k: v.item() if hasattr(v, 'item') else v for k, v in insights.items()}

    def process_and_analyze(self, input_data: Union[str, List[str]], input_type: str = 'text') -> Dict:
        # Use Gemini Vision to get raw transaction strings
        from pdf2data import process_document_with_gemini
        print('hello')
        try:
            print('Processing input data:', input_data)
            if isinstance(input_data, list):
                print('is a list')
                # Process each file path and combine results
                all_transactions = []
                for file_path in input_data:
                    try:
                        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
                        transactions = process_document_with_gemini(file_path, f'./all_csvs/output_{timestamp}.csv')
                        all_transactions.extend(transactions)
                    except Exception as e:
                        print(f"Error processing in  {file_path}: {e}")
                transactions = all_transactions
            else:
                print(input_data)
                timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
                transactions = process_document_with_gemini(input_data, f'./all_csvs/output_{timestamp}.csv')
                
            # Process these strings using existing text analyzer
            transactions_df = self.process_text_transactions(transactions)
            
            insights = self.generate_insights(transactions_df)
            
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            if not os.path.exists('./all_csvs'):
                os.makedirs('./all_csvs')
            transactions_df.to_csv(f'./all_csvs/processed_transactions_{timestamp}.csv', index=False)
            
            return {
                'transactions': transactions_df.to_dict('records'),
                'insights': insights
            }
        except Exception as e:
            print(e)

    def process_document(self, file_path: str) -> Dict:
        file_ext = os.path.splitext(file_path)[1].lower()
        print(f'Processing single file: {file_path}')
        
        if file_ext in ['.txt']:
            print('WE ARE HEREE')
            file_path = './' + file_path.replace('\\', '/')
            print(file_path)
            try:
                return self.process_and_analyze(file_path, 'text')
            except Exception as e:
                print(f"Error processing {file_path}: {e}")
                return {'error': str(e)}
        else:
            from pdf2data import process_document_with_gemini
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            return process_document_with_gemini(file_path, f'./all_csvs/output_{timestamp}.csv')


def main():
    processor = UPIDataProcessor()
    # upi_ids = input('Enter you UPI IDs seperated by commas: ').split(',')
    # for id in upi_ids:
    #     id = id.replace('@', '_')
    #     print(processor.process_document(f'./{id}_transactions.txt'))
    # # Example usage with text transactions
    # text_transactions = [
    #     "2024-01-20 INR 500 debited to swiggy.75839@okicici for dinner",
    #     "2024-01-21 INR 1000 credited from yash.gupta123@hdfc salary",
    #     "2024-01-22 INR 200 debited to 9876543210@paytm for groceries"
    # ]
    
    
    # results = processor.process_and_analyze(text_transactions, 'text')
    
    results = processor.process_document(f'./testing.pdf')
    print("\nProcessed Transactions:")
    print(pd.DataFrame(results['transactions']))
    print("\nInsights:")
    print(json.dumps(results['insights'], indent=2))

if __name__ == "__main__":
    main()
