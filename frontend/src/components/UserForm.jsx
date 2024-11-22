import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

const UserForm = () => {
  const navigate = useNavigate();
  const [currentStep, setCurrentStep] = useState(1);
  // Add this near the top with other state declarations
  const [applicationId, setApplicationId] = useState(null);

  const [formData, setFormData] = useState({
    loanPurpose: "",
    incomeSource: "",
    useUpi: "",
    offlineRecords: [], // Initialize as empty array
    documents: [], // Initialize as empty array
    upiEntries: [
        {
            upiId: '',
            transactionFile: null,
            isOwn: '',
            relationship: '',
            frequency: ''
        }
    ]
});
  

  const handleInputChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  

// Update handleFileChange to handle array initialization
const handleFileChange = (e) => {
    const files = Array.from(e.target.files || []); // Ensure files is an array
    setFormData({
        ...formData,
        [e.target.name]: files
    });
};


  const nextStep = () => {
    setCurrentStep(currentStep + 1);
  };

  const previousStep = () => {
    setCurrentStep(currentStep - 1);
  };

const handleSubmit = async (e) => {
  e.preventDefault();
  
  const formDataToSend = new FormData();
  
  // Append text data
  formDataToSend.append("loanPurpose", formData.loanPurpose);
  formDataToSend.append("incomeSource", formData.incomeSource);
  formDataToSend.append("useUpi", formData.useUpi);
  
  // Append UPI entries
  formData.upiEntries.forEach((entry, index) => {
      formDataToSend.append(`upiEntries[${index}][upiId]`, entry.upiId);
      formDataToSend.append(`upiEntries[${index}][isOwn]`, entry.isOwn);
      formDataToSend.append(`upiEntries[${index}][relationship]`, entry.relationship);
      formDataToSend.append(`upiEntries[${index}][frequency]`, entry.frequency);
    
      if (entry.transactionFile) {
          formDataToSend.append(`upiEntries[${index}][transactionFile]`, entry.transactionFile);
      }
  });
  
  // Add other files
  formData.offlineRecords.forEach(file => {
      formDataToSend.append('offlineRecords', file);
  });
    
  formData.documents.forEach(file => {
      formDataToSend.append('documents', file);
  });

  try {
      // Submit application
      const submitResponse = await fetch("http://127.0.0.1:5000/api/submit-loan-application", {
          method: "POST",
          body: formDataToSend,
      });
          if (submitResponse.ok) {
              const submitResult = await submitResponse.json();
              setApplicationId(submitResult.applicationId);
              alert("Application submitted successfully!");
              nextStep(); // Add this line to advance to step 6
      }
  } catch (error) {
      console.error("Error:", error);
      alert("An error occurred while submitting your application");
  }
};

const handleGenerateReport = async () => {
  try {
      console.log('in handleGenerateReport')
      const analysisResponse = await fetch("http://127.0.0.1:5000/api/analyze", {
          method: "POST",
          headers: {
              'Content-Type': 'application/json',
          },
          body: JSON.stringify({
              applicationId: applicationId
          }),
      });
        
      if (analysisResponse.ok) {
          const analysisResult = await analysisResponse.json();
          console.log(analysisResult);
          alert("Loan report generated successfully!");
          // Navigate to results page or show results modal
      }
  } catch (error) {
      console.error("Error generating report:", error);
      alert("An error occurred while generating the loan report");
  }
};

// Update the button in the form render section:

  const handleUpiEntryChange = (index, field, value) => {
    const newUpiEntries = [...formData.upiEntries];
    newUpiEntries[index] = {
      ...newUpiEntries[index],
      [field]: value
    };
    setFormData({
      ...formData,
      upiEntries: newUpiEntries
    });
  };
  
  const addNewUpiEntry = () => {
    setFormData({
      ...formData,
      upiEntries: [
        ...formData.upiEntries,
        {
          upiId: '',
          transactionFile: null,
          isOwn: '',
          relationship: '',
          frequency: ''
        }
      ]
    });
  };

  const renderStep = () => {
    switch(currentStep) {
      case 1:
        return (
          <div>
            <label className="block text-white font-semibold mb-2">
              Hi! Can you specify your loan purpose?
            </label>
            <textarea
              name="loanPurpose"
              value={formData.loanPurpose}
              onChange={handleInputChange}
              className="w-full p-4 border rounded-lg bg-white/5 border-white/20 text-white focus:ring-2 focus:ring-yellow-400 placeholder-white/50"
              placeholder="What will the funds be used for?"
              rows="3"
              required
            />
          </div>
        );
      
      case 2:
        return (
          <div>
            <label className="block text-white font-semibold mb-2">
              What's your primary income source?
            </label>
            <input
              type="text"
              name="incomeSource"
              value={formData.incomeSource}
              onChange={handleInputChange}
              className="w-full p-4 border rounded-lg bg-white/5 border-white/20 text-white focus:ring-2 focus:ring-yellow-400 placeholder-white/50"
              placeholder="Enter your main source of income"
              required
            />
          </div>
        );

        case 3:
        return (
            <div className="space-y-6">
            <div>
                <label className="block text-white font-semibold mb-2">
                Do you use UPI?
                </label>
                <select required = {true}
                name="useUpi"
                onChange={handleInputChange}
                className="w-full p-4 border rounded-lg bg-blue-900/50 border-yellow-400/50 text-white focus:ring-2 focus:ring-yellow-400 hover:border-yellow-400 cursor-pointer"
                >
                <option value="" className="bg-blue-900 text-white">Select an option</option>
                <option value="yes" className="bg-blue-900 text-white">Yes</option>
                <option value="no" className="bg-blue-900 text-white">No</option>
                </select>
            </div>

            {formData.useUpi === 'yes' && (
                <div className="space-y-8">
                {formData.upiEntries?.map((entry, index) => (
                    <div key={index} className="p-6 border border-white/20 rounded-lg space-y-4">
                    <div>
                        <label className="block text-white font-semibold mb-2">
                        UPI ID #{index + 1}
                        </label>
                        <input
                        type="text"
                        value={entry.upiId}
                        onChange={(e) => handleUpiEntryChange(index, 'upiId', e.target.value)}
                        className="w-full p-4 border rounded-lg bg-white/5 border-white/20 text-white focus:ring-2 focus:ring-yellow-400"
                        placeholder="Enter UPI ID"
                        />
                    </div>

                    <div>
                        <label className="block text-white font-semibold mb-2">
                        Upload Transaction File
                        </label>
                        <input
                        type="file"
                        onChange={(e) => handleUpiEntryChange(index, 'transactionFile', e.target.files[0])}
                        className="w-full p-4 border rounded-lg bg-white/5 border-white/20 text-white focus:ring-2 focus:ring-yellow-400"
                        accept=".txt,.pdf,.csv"
                        />
                    </div>

                    <div>
                        <label className="block text-white font-semibold mb-2">
                        Is this your UPI ID?
                        </label>
                        <select required = {true}
                        value={entry.isOwn}
                        onChange={(e) => handleUpiEntryChange(index, 'isOwn', e.target.value)}
                        className="w-full p-4 border rounded-lg bg-blue-900/50 border-yellow-400/50 text-white focus:ring-2 focus:ring-yellow-400 hover:border-yellow-400 cursor-pointer"
                        >
                        <option value="" className="bg-blue-900 text-white">Select</option>
                        <option value="yes" className="bg-blue-900 text-white">Yes</option>
                        <option value="no" className="bg-blue-900 text-white">No</option>
                        </select>
                    </div>

                    {entry.isOwn === 'no' && (
                        <div>
                        <label className="block text-white font-semibold mb-2">
                            What is your relationship with the UPI ID owner?
                        </label>
                        <input
                            type="text"
                            value={entry.relationship}
                            onChange={(e) => handleUpiEntryChange(index, 'relationship', e.target.value)}
                            className="w-full p-4 border rounded-lg bg-white/5 border-white/20 text-white focus:ring-2 focus:ring-yellow-400"
                            placeholder="Example: Brother, Friend, Family member"
                        />
                        </div>
                    )}

                    <div>
                        <label className="block text-white font-semibold mb-2">
                        How frequently do you use this UPI ID and for what purposes (Please specify for better results)?
                        </label>
                        <textarea
                        value={entry.frequency}
                        onChange={(e) => handleUpiEntryChange(index, 'frequency', e.target.value)}
                        className="w-full p-4 border rounded-lg bg-white/5 border-white/20 text-white focus:ring-2 focus:ring-yellow-400"
                        placeholder="Describe usage frequency and purposes"
                        rows="3"
                        />
                    </div>
                    </div>
                ))}

                <button
                    type="button"
                    onClick={addNewUpiEntry}
                    className="bg-yellow-400 text-blue-900 px-6 py-2 rounded-full font-bold hover:bg-yellow-300 transition duration-300"
                >
                    + Add Another UPI ID
                </button>
                </div>
            )}
            </div>
        );

          

      case 4:
        return (
          <div>
            <label className="block text-white font-semibold mb-2">
              Upload offline transaction records (bills, checks, khatabook etc.)
            </label>
            <input
              type="file"
              name="offlineRecords"
              onChange={handleFileChange}
              className="w-full p-4 border rounded-lg bg-white/5 border-white/20 text-white focus:ring-2 focus:ring-yellow-400"
              multiple
              accept=".pdf,.png,.jpg,.jpeg,.doc,.docx"
            />
          </div>
        );

      case 5:
        return (
          <div>
            <label className="block text-white font-semibold mb-2">
              Upload Identity Documents (KYC, Aadhar, PAN, etc.)
            </label>
            <input
              type="file"
              name="documents"
              onChange={handleFileChange}
              className="w-full p-4 border rounded-lg bg-white/5 border-white/20 text-white focus:ring-2 focus:ring-yellow-400"
              multiple
              accept=".pdf,.png,.jpg,.jpeg"
            />
          </div>
        );
        case 6:
          return (
            <div>
              <h3 className="text-2xl text-white font-bold mb-4">
                Ready to Generate Your Loan Report
              </h3>
              <p className="text-white mb-4">
                Click the button below to analyze your submitted information and generate a comprehensive loan report.
              </p>
            </div>
          );
        default:
          return null;
      }
  };

  return (
    <div className="bg-gradient-to-r from-blue-600 to-blue-800 py-12 min-h-screen">
      <div className="container mx-auto px-4 max-w-2xl">
        <h2 className="text-5xl font-extrabold text-white mb-6 text-center leading-tight">
          Get Your <span className="text-yellow-400">Smart Loan Report</span>
        </h2>
        <p className="text-xl text-blue-100 mb-8 text-center max-w-2xl mx-auto">
          Let our AI analyze your profile and create a perfect loan application package
        </p>

        <form onSubmit={handleSubmit} className="space-y-6">
          <div className="bg-white/10 backdrop-blur-lg rounded-lg p-8 space-y-6">
            {renderStep()}
          </div>

          <div className="text-center pt-6 flex justify-center gap-4">
    {currentStep > 1 && (
        <button
        type="button"
        onClick={previousStep}
        className="bg-blue-500 text-white px-12 py-4 rounded-full font-bold text-lg hover:bg-blue-600 transition duration-300 shadow-lg"
        >
        Previous
        </button>
    )}
    {currentStep < 5 ? (
        <button
        type="button"
        onClick={nextStep}
        className="bg-yellow-400 text-blue-900 px-12 py-4 rounded-full font-bold text-lg hover:bg-yellow-300 transition duration-300 shadow-lg"
        >
        Next
        </button>
    ) : currentStep < 6 ? (
        <button
        type="submit"
        onClick={handleSubmit}
        className="bg-yellow-400 text-blue-900 px-12 py-4 rounded-full font-bold text-lg hover:bg-yellow-300 transition duration-300 shadow-lg"
        >
        Submit Application
        </button>
    ) : currentStep === 6 && (
        <button
        type="button"
        onClick={handleGenerateReport}
        className="bg-green-500 text-white px-12 py-4 rounded-full font-bold text-lg hover:bg-green-600 transition duration-300 shadow-lg"
        >
        Generate Loan Report
        </button>
    )}
</div>


        </form>
      </div>
    </div>
  );
};

export default UserForm;
