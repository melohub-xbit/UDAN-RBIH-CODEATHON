import React, { useState, useEffect } from 'react';
// import Papa from 'papaparse';
// import csvData from '../../../backendv2/uploaded_files/loan_application_20241121_095130.csv'
const Dashboard = () => {
  const [transactions, setTransactions] = useState([]);
  const [query, setQuery] = useState('');
  const [queryResult, setQueryResult] = useState('');
  const [report, setReport] = useState('');
  const [loading, setLoading] = useState(false);
  const [pdfUrl, setPdfUrl] = useState('');

//   useEffect(() => {
//     Papa.parse(csvData, {
//       header: true,
//       download: true,
//       complete: (results) => {
//         setTransactions(results.data);
//       },
//     });
//   }, []);

  const handleQuery = async () => {
    setLoading(true);
    try {
      const response = await fetch('http://127.0.0.1:5000/api/query-transactions', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ question: query }),
      });
      const data = await response.json();
      setQueryResult(data.result);
    } catch (error) {
      console.error('Error:', error);
    }
    setLoading(false);
  };

  const generateReport = async () => {
    setLoading(true);
    try {
      const response = await fetch('http://127.0.0.1:5000/api/generate-report');
      const data = await response.json();
      setReport(data.report);
    } catch (error) {
      console.error('Error:', error);
    }
    setLoading(false);
  };

  return (
    <div className="bg-gradient-to-r from-blue-600 to-blue-800 min-h-screen py-12">
      <div className="container mx-auto px-4">
        <h1 className="text-4xl font-extrabold text-white mb-8 text-center">
          Financial <span className="text-yellow-400">Dashboard</span>
        </h1>

        {/* Query Section */}
        <div className="bg-white rounded-lg p-6 mb-8">
          <h2 className="text-2xl font-bold mb-4">Ask About Your Transactions</h2>
          <div className="flex gap-4 mb-4">
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Ask any question about your transactions..."
              className="flex-1 p-3 border rounded-lg"
            />
            <button
              onClick={handleQuery}
              disabled={loading}
              className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700"
            >
              {loading ? 'Processing...' : 'Ask'}
            </button>
          </div>
          {queryResult && (
            <div className="bg-gray-50 p-4 rounded-lg">
              <h3 className="font-bold mb-2">Answer:</h3>
              <p>{queryResult}</p>
            </div>
          )}
        </div>

        {/* Report Section */}
        <div className="bg-white rounded-lg p-6 mb-8">
          <div className="flex justify-between items-center mb-4">
            <h2 className="text-2xl font-bold">Financial Report</h2>
            <button
              onClick={generateReport}
              disabled={loading}
              className="bg-yellow-400 text-blue-900 px-6 py-2 rounded-lg hover:bg-yellow-300"
            >
              {loading ? 'Generating...' : 'Generate Report'}
            </button>
          </div>
          {report && (
            <div className="space-y-4">
                <div className="bg-gray-50 p-4 rounded-lg whitespace-pre-wrap">
                    {report}
                </div>
                {pdfUrl && (
                    <div className="mt-4">
                        <h3 className="font-bold mb-2">PDF Report</h3>
                        <iframe
                            src={`http://127.0.0.1:5000${pdfUrl}`}
                            className="w-full h-96 border rounded-lg"
                            title="Financial Report PDF"
                        />
                        <a 
                            href={`http://127.0.0.1:5000${pdfUrl}`}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="mt-2 inline-block bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
                        >
                            Download PDF
                        </a>
                    </div>
                )}
            </div>
          )}
        </div>

        {/* Transactions Table */}
        <div className="bg-white bg-opacity-95 rounded-lg shadow-lg overflow-hidden">
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-blue-900 text-white">
                <tr>
                  <th className="px-6 py-3 text-left">Date & Time</th>
                  <th className="px-6 py-3 text-left">Transaction Type</th>
                  <th className="px-6 py-3 text-left">Amount</th>
                  <th className="px-6 py-3 text-left">Category</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-200">
                {transactions.map((transaction, index) => (
                  <tr key={index} className="hover:bg-blue-50">
                    <td className="px-6 py-4">{transaction.date}</td>
                    <td className="px-6 py-4">{transaction.transaction_type}</td>
                    <td className={`px-6 py-4 ${
                      transaction.amount < 0 ? 'text-red-600' : 'text-green-600'
                    }`}>
                      ₹{Math.abs(transaction.amount)}
                    </td>
                    <td className="px-6 py-4">{transaction.category}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
