import React, { useState } from "react";

const TransactionAnalysis = () => {
  const [results, setResults] = useState(null);
  const [transactions] = useState([
    "2024-01-20 INR 500 debited to swiggy.75839@okicici for dinner",
    "2024-01-21 INR 1000 credited from yash.gupta123@hdfc salary"
  ]);

  const fetchAnalysis = async () => {
    try {
      const response = await fetch('http://localhost:5000/api/analyze', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ transactions })
      });
      
      const data = await response.json();
      setResults(data);
    } catch (error) {
      console.error('Error:', error);
    }
  };

  return (
    <div className="bg-gradient-to-r from-blue-600 to-blue-800 py-24">
      <div className="container mx-auto text-center px-4">
        <h1 className="text-5xl font-extrabold text-white mb-6 leading-tight">
          Transaction <span className="text-yellow-400">Analysis</span>
        </h1>

        <button 
          onClick={fetchAnalysis}
          className="bg-yellow-400 text-blue-900 px-8 py-3 rounded-full font-bold hover:bg-yellow-300 transition duration-300 mb-8"
        >
          Analyze Transactions
        </button>

        {results && (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8 max-w-4xl mx-auto">
            <div className="bg-white p-8 rounded-lg shadow-lg">
              <h2 className="text-2xl font-bold text-blue-800 mb-6">Transactions</h2>
              <div className="space-y-4">
                {results.transactions.map((tx, index) => (
                  <div key={index} className="border-b pb-4">
                    <p className="text-left">Amount: ₹{tx.amount}</p>
                    <p className="text-left">Category: {tx.category}</p>
                    <p className="text-left">Bank: {tx.bank}</p>
                  </div>
                ))}
              </div>
            </div>

            <div className="bg-white p-8 rounded-lg shadow-lg">
              <h2 className="text-2xl font-bold text-blue-800 mb-6">Insights</h2>
              <div className="space-y-4 text-left">
                <p>Total Transactions: {results.insights.total_transactions}</p>
                <p>Total Amount: ₹{results.insights.total_amount}</p>
                <p>Average Transaction: ₹{results.insights.avg_transaction}</p>
                <div>
                  <h3 className="font-bold mt-4">Category Distribution</h3>
                  {Object.entries(results.insights.category_distribution).map(([category, count]) => (
                    <p key={category}>{category}: {count}</p>
                  ))}
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default TransactionAnalysis;
