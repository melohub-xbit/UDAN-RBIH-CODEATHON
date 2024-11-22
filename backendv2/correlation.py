import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

def analyze_transactions_comparison(manish_csv, brother_csv):
    # Ensure output directory exists
    os.makedirs('transaction_analysis', exist_ok=True)
    
    # Read CSV files
    df_manish = pd.read_csv(manish_csv, parse_dates=['date'])
    df_brother = pd.read_csv(brother_csv, parse_dates=['date'])
    
    # Group by month and category, calculate total spending
    df_manish_monthly = df_manish.groupby([df_manish['date'].dt.to_period('M'), 'category'])['amount'].sum().unstack(fill_value=0)
    df_brother_monthly = df_brother.groupby([df_brother['date'].dt.to_period('M'), 'category'])['amount'].sum().unstack(fill_value=0)
    
    # Convert Period index to datetime for plotting
    df_manish_monthly.index = df_manish_monthly.index.to_timestamp()
    df_brother_monthly.index = df_brother_monthly.index.to_timestamp()
    
    # Ensure both DataFrames have the same categories
    common_categories = list(set(df_manish_monthly.columns) & set(df_brother_monthly.columns))
    df_manish_monthly = df_manish_monthly[common_categories]
    df_brother_monthly = df_brother_monthly[common_categories]
    
    # Correlation of monthly spending by category
    correlation_matrix = df_manish_monthly.corrwith(df_brother_monthly)
    
    # Visualization 1: Correlation Bar Plot
    plt.figure(figsize=(12, 6))
    correlation_matrix.plot(kind='bar')
    plt.title('Correlation of Spending Categories between Manish and Brother')
    plt.xlabel('Categories')
    plt.ylabel('Correlation Coefficient')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('transaction_analysis/category_correlation.png')
    plt.close()
    
    # Visualization 2: Monthly Spending Comparison
    plt.figure(figsize=(14, 7))
    df_manish_monthly.sum(axis=1).plot(label='Manish', marker='o')
    df_brother_monthly.sum(axis=1).plot(label='Brother', marker='x')
    plt.title('Monthly Total Spending Comparison')
    plt.xlabel('Month')
    plt.ylabel('Total Spending')
    plt.legend()
    plt.tight_layout()
    plt.savefig('transaction_analysis/monthly_spending_comparison.png')
    plt.close()
    
    # Visualization 3: Category-wise Spending Comparison
    plt.figure(figsize=(15, 8))
    for category in common_categories:
        plt.plot(df_manish_monthly.index, df_manish_monthly[category], 
                 label=f'Manish {category}', alpha=0.5)
        plt.plot(df_brother_monthly.index, df_brother_monthly[category], 
                 label=f'Brother {category}', linestyle='--', alpha=0.5)
    plt.title('Category-wise Monthly Spending Comparison')
    plt.xlabel('Month')
    plt.ylabel('Spending Amount')
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.savefig('transaction_analysis/category_spending_comparison.png')
    plt.close()
    
    # Print detailed analysis
    print("\nSpending Category Correlation Analysis:")
    print(correlation_matrix)
    
    # Overall spending correlation
    overall_correlation = np.corrcoef(df_manish_monthly.sum(axis=1), df_brother_monthly.sum(axis=1))[0, 1]
    print(f"\nOverall Monthly Spending Correlation: {overall_correlation:.4f}")
    
    # Total spending by category
    print("\nManish - Total Spending by Category:")
    print(df_manish_monthly.sum())
    print("\nBrother - Total Spending by Category:")
    print(df_brother_monthly.sum())
    
    # Aggregate statistics
    print("\nAggregate Statistics:")
    print("Manish Total Spending:", df_manish['amount'].sum())
    print("Brother Total Spending:", df_brother['amount'].sum())
    print("Manish Average Transaction:", df_manish['amount'].mean())
    print("Brother Average Transaction:", df_brother['amount'].mean())

def main():
    # Prompt for file paths
    manish_csv = "./transaction_analysis/manish_transactions.csv"
    brother_csv = "./transaction_analysis/brother_transactions.csv"
    
    analyze_transactions_comparison(manish_csv, brother_csv)

if __name__ == "__main__":
    main()