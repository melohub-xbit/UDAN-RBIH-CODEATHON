import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

# Load the dataset (replace with the actual CSV file path)
file_path = "filled_transactions.csv"  # Adjust if needed
data = pd.read_csv(file_path)

# Convert the 'date' column to datetime and sort by date
data['date'] = pd.to_datetime(data['date'])
data = data.sort_values('date').reset_index(drop=True)

# Plot the date vs. amount graph
plt.figure(figsize=(12, 6))
plt.plot(data['date'], data['amount'], marker='o', linestyle='-', label='Amount')
plt.title("Date vs Amount")
plt.xlabel("Date")
plt.ylabel("Amount")
plt.grid()
plt.legend()
plt.show()

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
print(f"Total Predicted Amount for the Next Month: {next_month_total}")

# Determine profit or loss
if next_month_total > 0:
    print("The prediction for the next month is PROFIT.")
else:
    print("The prediction for the next month is LOSS.")

# Plot historical data with predictions for the next month
plt.figure(figsize=(12, 6))
plt.plot(data['date'], data['amount'], marker='o', label='Actual Amount')
future_dates = [data['date'].max() + pd.Timedelta(days=i) for i in range(1, 31)]

