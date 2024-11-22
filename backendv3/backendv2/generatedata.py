import random
import datetime
import matplotlib.pyplot as plt
import os
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

# Ensure output directory exists
os.makedirs('transaction_analysis', exist_ok=True)

def generate_random_upi():
    providers = ['okhdfc', 'oksbi', 'okicici', 'okaxis', 'paytm']
    names = ['store', 'shop', 'mart', 'retail', 'market', 'vendor', 'seller']
    numbers = [f"{random.randint(100, 999)}" for _ in range(3)]
    return f"{random.choice(names)}.{random.choice(numbers)}@{random.choice(providers)}"

# Categories for Manish (categories_a) and his brother (categories_b)
categories_a = {
    "business": [(generate_random_upi(), 10, 45) for _ in range(6)],
    "electricity": [(generate_random_upi(), 10, 30) for _ in range(6)],
    "water": [(generate_random_upi(), 5, 20) for _ in range(6)],
    "phone": [(generate_random_upi(), 5, 15) for _ in range(6)],
    "internet": [(generate_random_upi(), 10, 40) for _ in range(6)],
    "gas": [(generate_random_upi(), 10, 30) for _ in range(6)],
    "groceries": [(generate_random_upi(), 5, 25) for _ in range(6)],
    "transport": [(generate_random_upi(), 3, 15) for _ in range(6)]
}

categories_b = {
    "business": [(generate_random_upi(), 15, 48) for _ in range(5)],
    "electricity": [(generate_random_upi(), 12, 32) for _ in range(5)],
    "water": [(generate_random_upi(), 7, 22) for _ in range(5)],
    "phone": [(generate_random_upi(), 6, 17) for _ in range(5)],
    "internet": [(generate_random_upi(), 12, 42) for _ in range(6)],
    "gas": [(generate_random_upi(), 10, 28) for _ in range(5)],
    "groceries": [(generate_random_upi(), 7, 27) for _ in range(5)],
    "transport": [(generate_random_upi(), 4, 17) for _ in range(5)]
}

def generate_transactions(categories, s, num_months=12):
    transactions = []
    start_date = datetime.datetime.now() - datetime.timedelta(days=num_months * 30)
    transaction_prob = 0.4 if s == 'a' else 0.12

    for day in range(num_months * 30):
        category = "business" if random.random() < transaction_prob else random.choice(list(categories.keys()))
        bill_date = start_date + datetime.timedelta(days=day)
        payee, min_amount, max_amount = random.choice(categories[category])
        amount = random.randint(min_amount, max_amount)
        
        transaction = {
            'date': bill_date,
            'amount': amount,
            'category': category,
            'payee': payee
        }
        transactions.append(transaction)

    return sorted(transactions, key=lambda x: x['date'])

def save_transactions_to_file(transactions, filename):
    with open(filename, 'w') as file:
        for t in transactions:
            date_str = t['date'].strftime('%H:%M:%S %d-%m-%Y')
            file.write(f"[{date_str}] INR {t['amount']} debited to {t['payee']}\n")

def save_transactions_to_csv(transactions, filename):
    # Convert transactions to a DataFrame and save as CSV
    df = pd.DataFrame(transactions)
    df['date'] = pd.to_datetime(df['date'])
    df.to_csv(filename, index=False)

def plot_detailed_transactions(transactions, title):
    plt.figure(figsize=(20, 10))
    
    # Category-wise spending
    plt.subplot(2, 2, 1)
    categories_data = {}
    for t in transactions:
        categories_data[t['category']] = categories_data.get(t['category'], 0) + t['amount']
    
    plt.pie(categories_data.values(), labels=categories_data.keys(), autopct='%1.1f%%')
    plt.title(f'{title} - Expense Categories')
    
    # business transactions over time
    plt.subplot(2, 2, 2)
    business_transactions = [t for t in transactions if t['category'] == 'business']
    business_amounts = [t['amount'] for t in business_transactions]
    business_dates = [t['date'] for t in business_transactions]
    plt.scatter(business_dates, business_amounts)
    plt.title(f'{title} - business Transactions')
    plt.xlabel('Date')
    plt.ylabel('Amount (INR)')
    plt.xticks(rotation=45)
    
    # Monthly total spending
    plt.subplot(2, 2, 3)
    monthly_spending = {}
    for t in transactions:
        month_key = t['date'].strftime('%Y-%m')
        monthly_spending[month_key] = monthly_spending.get(month_key, 0) + t['amount']
    
    months = sorted(monthly_spending.keys())
    spending_values = [monthly_spending[month] for month in months]
    plt.plot(months, spending_values, marker='o')
    plt.title(f'{title} - Monthly Total Spending')
    plt.xlabel('Month')
    plt.ylabel('Total Amount (INR)')
    plt.xticks(rotation=45)
    
    # Transaction frequency by category
    plt.subplot(2, 2, 4)
    category_frequency = {}
    for t in transactions:
        category_frequency[t['category']] = category_frequency.get(t['category'], 0) + 1
    
    plt.bar(category_frequency.keys(), category_frequency.values())
    plt.title(f'{title} - Transaction Frequency')
    plt.xlabel('Category')
    plt.ylabel('Number of Transactions')
    plt.xticks(rotation=45)
    
    plt.tight_layout()
    
    # Save the figure
    filename = f'transaction_analysis/{title.lower().replace(" ", "_")}_analysis.png'
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    plt.close()

def predict_transactions(file_path):
    # Load the dataset
    data = pd.read_csv(file_path)
    
    # Convert the 'date' column to datetime and sort by date
    data['date'] = pd.to_datetime(data['date'])
    data = data.sort_values('date').reset_index(drop=True)
    
    # Prepare data for Random Forest model
    # Convert dates to numeric (days since start) for modeling
    data['days'] = (data['date'] - data['date'].min()).dt.days
    X = data[['days']]  # Feature
    y = data['amount']  # Target
    
    # Split into training and test sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Train the Random Forest Regressor
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    # Predict the amounts for the next month (30 days)
    last_day = data['days'].max()
    future_days = np.arange(last_day + 1, last_day + 31).reshape(-1, 1)
    future_predictions = model.predict(future_days)
    
    # Calculate the total predicted amount for the next month
    next_month_total = future_predictions.sum()
    
    # Create visualization of historical and predicted data
    plt.figure(figsize=(12, 6))
    plt.plot(data['date'], data['amount'], marker='o', label='Actual Amount')
    future_dates = [data['date'].max() + pd.Timedelta(days=i) for i in range(1, 31)]
    #plt.scatter(future_dates, future_predictions, color='red', label='Predicted Amount')
    plt.title("Historical and Predicted Transactions")
    plt.xlabel("Date")
    plt.ylabel("Amount")
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('transaction_analysis/prediction_plot.png')
    plt.close()
    
    # Print prediction results
    print(f"Total Predicted Amount for the Next Month: INR {next_month_total:.2f}")
    print("Prediction for the next month is: " + 
          ("PROFIT" if next_month_total > 0 else "LOSS"))
    
    return next_month_total

def main():
    # Generate transactions for Manish and his brother
    manish_transactions = generate_transactions(categories_a, 'a')
    brother_transactions = generate_transactions(categories_b, 'b')
    
    # Save transactions to files
    save_transactions_to_file(manish_transactions, 'manish.txt')
    save_transactions_to_file(brother_transactions, 'brother.txt')
    
    # Save transactions to CSV for prediction
    save_transactions_to_csv(manish_transactions, 'transaction_analysis/manish_transactions.csv')
    save_transactions_to_csv(brother_transactions, 'transaction_analysis/brother_transactions.csv')
    
    # Plot the transactions
    plot_detailed_transactions(manish_transactions, "Manish's Transactions")
    plot_detailed_transactions(brother_transactions, "Brother's Transactions")
    
    # Predict transactions for both Manish and his brother
    print("Prediction for Manish's Transactions:")
    manish_prediction = predict_transactions('transaction_analysis/manish_transactions.csv')
    
    print("\nPrediction for Brother's Transactions:")
    brother_prediction = predict_transactions('transaction_analysis/brother_transactions.csv')
    
    print("\nTransaction Analysis Complete.")

if __name__ == "__main__":
    main()