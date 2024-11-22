import React, { useState } from 'react';
import styled from 'styled-components';

const FormContainer = styled.div`
  max-width: 800px;
  margin: 2rem auto;
  padding: 2rem;
  background: white;
  border-radius: 15px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
`;

const Section = styled.div`
  margin-bottom: 2rem;
`;

const CheckboxGroup = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 1rem;
`;

const Question = styled.div`
  margin-bottom: 1.5rem;
`;

// Get unique documents from both JSON files
const getAllUniqueDocuments = (agriLoans, msmeLoans) => {
  const allDocs = new Set();
  [...agriLoans, ...msmeLoans].forEach(loan => {
    loan.documents.forEach(doc => allDocs.add(doc));
  });
  return Array.from(allDocs);
};

const LoanEligibilityChecker = ({ agriLoans, msmeLoans }) => {
  const [userDocuments, setUserDocuments] = useState(new Set());
  const [businessInfo, setBusinessInfo] = useState({
    type: '',
    size: '',
    sector: '',
    annualTurnover: '',
    ownership: ''
  });

  const handleDocumentCheck = (doc) => {
    const newDocs = new Set(userDocuments);
    if (newDocs.has(doc)) {
      newDocs.delete(doc);
    } else {
      newDocs.add(doc);
    }
    setUserDocuments(newDocs);
  };

  const findEligibleLoans = () => {
    const allLoans = [...agriLoans, ...msmeLoans];
    return allLoans.filter(loan => {
      const hasRequiredDocs = loan.documents.every(doc => userDocuments.has(doc));
      
      // Add business-specific matching logic here
      const matchesSector = businessInfo.sector.toLowerCase().includes(loan.target_group.toLowerCase());
      
      return hasRequiredDocs && matchesSector;
    });
  };

  return (
    <FormContainer>
      <h1 className="text-3xl font-bold mb-6">Loan Eligibility Checker</h1>
      
      <Section>
        <h2 className="text-xl font-semibold mb-4">Business Information</h2>
        <Question>
          <label>Business Type</label>
          <select 
            className="w-full p-2 border rounded"
            value={businessInfo.type}
            onChange={(e) => setBusinessInfo({...businessInfo, type: e.target.value})}
          >
            <option value="">Select Business Type</option>
            <option value="agriculture">Agriculture</option>
            <option value="msme">MSME</option>
            <option value="retail">Retail</option>
            <option value="service">Service</option>
          </select>
        </Question>

        {/* Add more business-related questions */}
      </Section>

      <Section>
        <h2 className="text-xl font-semibold mb-4">Available Documents</h2>
        <CheckboxGroup>
          {getAllUniqueDocuments(agriLoans, msmeLoans).map((doc, index) => (
            <label key={index} className="flex items-center space-x-2">
              <input
                type="checkbox"
                checked={userDocuments.has(doc)}
                onChange={() => handleDocumentCheck(doc)}
                className="form-checkbox"
              />
              <span>{doc}</span>
            </label>
          ))}
        </CheckboxGroup>
      </Section>

      <button 
        className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 transition"
        onClick={() => {
          const eligibleLoans = findEligibleLoans();
          // Display eligible loans
        }}
      >
        Check Eligible Loans
      </button>
    </FormContainer>
  );
};

export default LoanEligibilityChecker   ;
