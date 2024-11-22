import random
import datetime

def generate_random_upi():
    providers = ['okhdfc', 'oksbi', 'okicici', 'okaxis', 'paytm']
    names = ['store', 'shop', 'mart', 'retail', 'market', 'vendor', 'seller']
    numbers = [f"{random.randint(100, 999)}" for _ in range(3)]
    return f"{random.choice(names)}.{random.choice(numbers)}@{random.choice(providers)}"

# Categories and payment ranges with random UPI IDs
categories = {
    "farm_purchase": [(generate_random_upi(), 5000, 15000) for _ in range(5)],
    "resale": [(generate_random_upi(), 7000, 20000) for _ in range(5)],
    "personal": [(generate_random_upi(), 200, 800) for _ in range(5)],
    "household": [(generate_random_upi(), 500, 1500) for _ in range(5)],
    "utilities": [(generate_random_upi(), 800, 1200) for _ in range(3)],
    "medical": [(generate_random_upi(), 300, 3000) for _ in range(4)],
    "clothing": [(generate_random_upi(), 800, 5000) for _ in range(4)],
    "education": [(generate_random_upi(), 2000, 25000) for _ in range(3)],
    "transport": [(generate_random_upi(), 100, 2000) for _ in range(4)],
    "food": [(generate_random_upi(), 200, 1000) for _ in range(5)],
    "entertainment": [(generate_random_upi(), 200, 2000) for _ in range(3)]
}

# Special categories with specific intervals
special_categories = {
    "electricity_bill": (generate_random_upi(), 800, 1200, 30),
    "water_bill": (generate_random_upi(), 500, 1000, 30),
    "phone_recharge": (generate_random_upi(), 300, 600, 30),
    "internet_bill": (generate_random_upi(), 700, 1500, 30),
    "gas_bill": (generate_random_upi(), 500, 1000, 30)
}

# Updated profiles with new categories
upi_profiles = [
    {
        "upi_id": "manish871246702@okhdfc",
        "role": "Shop Owner",
        "patterns": ["resale", "personal", "utilities", "transport", "food"],
        "special": ["electricity_bill", "water_bill", "internet_bill"]
    },
    {
        "upi_id": "7008921472@oksbi",
        "role": "Brother",
        "patterns": ["household", "utilities", "personal", "clothing", "education", "food"],
        "special": ["electricity_bill", "water_bill", "gas_bill"]
    }
]

def generate_transaction(upi_id, category, start_date):
    txn_date = start_date + datetime.timedelta(days=random.randint(0, 60))
    time = f"{random.randint(0, 23):02}:{random.randint(0, 59):02}:{random.randint(0, 59):02}"
    txn_datetime = txn_date.strftime(f"{time} %d-%m-%Y")
    
    payee, min_amount, max_amount = random.choice(categories[category])
    amount = random.randint(min_amount, max_amount)
    debit_credit = "debited to" if random.random() > 0.3 else "credited from"
    
    return f"[{txn_datetime}] INR {amount} {debit_credit} {payee}"

def generate_repeating_transactions(upi_id, special, start_date, num_months):
    transactions = []
    days_in_month = num_months * 30
    for category in special:
        payee, min_amount, max_amount, interval = special_categories[category]
        current_date = start_date
        while (current_date - start_date).days < days_in_month:
            time = f"{random.randint(0, 23):02}:{random.randint(0, 59):02}:{random.randint(0, 59):02}"
            txn_datetime = current_date.strftime(f"{time} %d-%m-%Y")
            amount = random.randint(min_amount, max_amount)
            transaction = f"[{txn_datetime}] INR {amount} debited to {payee}"
            transactions.append({"upi_id": upi_id, "transaction": transaction})
            current_date += datetime.timedelta(days=interval)
    return transactions

def generate_data(profiles, num_months=2):
    data = []
    start_date = datetime.datetime.now() - datetime.timedelta(days=num_months * 30)
    
    for profile in profiles:
        for _ in range(30):
            category = random.choice(profile["patterns"])
            transaction = generate_transaction(profile["upi_id"], category, start_date)
            data.append({"upi_id": profile["upi_id"], "role": profile["role"], "transaction": transaction})
        
        special_transactions = generate_repeating_transactions(
            profile["upi_id"], profile.get("special", []), start_date, num_months
        )
        for special_txn in special_transactions:
            special_txn["role"] = profile["role"]
        data.extend(special_transactions)
    
    return data

def save_to_txt(data):
    # Group transactions by UPI ID
    upi_transactions = {}
    for transaction in data:
        upi_id = transaction['upi_id']
        if upi_id not in upi_transactions:
            upi_transactions[upi_id] = []
        upi_transactions[upi_id].append(transaction)
    
    # Save each UPI ID's transactions to a separate file
    for upi_id, transactions in upi_transactions.items():
        # Sort transactions by timestamp
        sorted_transactions = sorted(transactions, key=lambda x: datetime.datetime.strptime(
            x['transaction'].split(']')[0][1:], 
            "%H:%M:%S %d-%m-%Y"
        ))
        
        # Create filename based on UPI ID (replacing special characters)
        filename = f"{upi_id.replace('@', '_').replace('.', '_')}_transactions.txt"
        
        with open(filename, mode="w") as file:
            for transaction in sorted_transactions:
                line = f"{transaction['role']} - {transaction['transaction']}"
                file.write(line + "\n")
        print(f"Generated transactions for {upi_id} in {filename}")

if __name__ == "__main__":
    transactions = generate_data(upi_profiles, num_months=24)
    save_to_txt(transactions)
    print(f"Generated transactions for {len(upi_profiles)} profiles")