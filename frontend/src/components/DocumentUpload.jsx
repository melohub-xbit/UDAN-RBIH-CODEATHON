import React, { useState } from "react";

const DocumentUpload = () => {
  const [upiId, setUpiId] = useState("");
  const [uploadStatus, setUploadStatus] = useState("");
  const [selectedFile, setSelectedFile] = useState(null);
  const [analysisResults, setAnalysisResults] = useState(null);

  const handleUpiSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch('http://localhost:5000/api/accepttext', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ upiId }),
      });

      const data = await response.json();
      setUploadStatus('UPI ID submitted successfully!');
      setUpiId('');
    } catch (error) {
      setUploadStatus('Error submitting UPI ID');
      console.error('Error:', error);
    }
  };

  const handleTransactionSubmit = async (e) => {
    e.preventDefault();
    if (!selectedFile) {
      setUploadStatus('Please select a file first');
      return;
    }
  
    try {
      // First check if UPI ID exists by making a test request
      const testResponse = await fetch('http://localhost:5000/api/accepttext', {
        method: 'GET'
      });
      
      if (!testResponse.ok) {
        setUploadStatus('Please enter your UPI ID first');
        return;
      }
  
      const fileReader = new FileReader();
      fileReader.onload = async (e) => {
        try {
          const text = e.target.result;
          const transactions = text.split('\n').filter(line => line.trim());
          
          const response = await fetch('http://localhost:5000/api/analyze', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({ transactions }),
          });
          
          if (!response.ok) {
            const errorData = await response.json();
            setUploadStatus(errorData.error || 'Please enter your UPI ID first');
            return;
          }
          
          const data = await response.json();
          setAnalysisResults(data);
          setUploadStatus('Transactions processed successfully!');
          setSelectedFile(null);
        } catch (innerError) {
          setUploadStatus('Please enter your UPI ID before uploading transactions');
        }
      };
      
      fileReader.readAsText(selectedFile);
    } catch (error) {
      setUploadStatus('Please enter your UPI ID before uploading transactions');
    }
  };
  

  return (
    <div className="bg-gradient-to-r from-blue-600 to-blue-800 min-h-screen py-24 relative z-10">
      <div className="container mx-auto text-center px-4 pb-24">
        <h1 className="text-5xl font-extrabold text-white mb-6 leading-tight">
          Transaction <span className="text-yellow-400">Upload</span>
        </h1>

        {uploadStatus && (
          <div className="mb-6 text-white bg-blue-500 p-3 rounded-lg max-w-md mx-auto">
            {uploadStatus}
          </div>
        )}

        <div className="grid grid-cols-1 md:grid-cols-2 gap-8 max-w-4xl mx-auto mt-12">
          <div className="bg-white p-8 rounded-lg shadow-lg">
            <h2 className="text-2xl font-bold text-blue-800 mb-6">Upload Transactions</h2>
            <form onSubmit={handleTransactionSubmit} className="space-y-4">
              <input
                type="file"
                accept=".txt"
                onChange={(e) => setSelectedFile(e.target.files[0])}
                className="w-full p-4 border rounded-lg"
              />
              <button
                type="submit"
                className="bg-yellow-400 text-blue-900 px-8 py-3 rounded-full font-bold hover:bg-yellow-300 transition duration-300 w-full"
              >
                Process Transactions
              </button>
            </form>
          </div>


          <div className="bg-white p-8 rounded-lg shadow-lg">
            <h2 className="text-2xl font-bold text-blue-800 mb-6">UPI Details</h2>
            <form onSubmit={handleUpiSubmit} className="space-y-4">
              <input
                type="text"
                value={upiId}
                onChange={(e) => setUpiId(e.target.value)}
                placeholder="Enter UPI ID"
                className="px-4 py-3 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500 w-full"
              />
              <button
                type="submit"
                className="bg-yellow-400 text-blue-900 px-8 py-3 rounded-full font-bold hover:bg-yellow-300 transition duration-300 w-full"
              >
                Submit UPI ID
              </button>
            </form>
          </div>
        </div>

        {analysisResults && (
          <div className="mt-12 mb-24">
            <h2 className="text-4xl font-bold text-white mb-8">
              Analysis <span className="text-yellow-400">Results</span>
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-8 max-w-4xl mx-auto">
              <div className="bg-white p-8 rounded-lg shadow-lg">
                <h2 className="text-2xl font-bold text-blue-800 mb-6">Transactions</h2>
                <div className="space-y-4">
                  {analysisResults.transactions.map((tx, index) => (
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
                  <p>Total Transactions: {analysisResults.insights.total_transactions}</p>
                  <p>Total Amount: ₹{analysisResults.insights.total_amount}</p>
                  <p>Average Transaction: ₹{analysisResults.insights.avg_transaction}</p>
                  <div>
                    <h3 className="font-bold mt-4">Category Distribution</h3>
                    {Object.entries(analysisResults.insights.category_distribution).map(([category, count]) => (
                      <p key={category}>{category}: {count}</p>
                    ))}
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default DocumentUpload;