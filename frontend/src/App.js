import React from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import Navbar from "./components/Navbar";
import HeroSection from "./components/HeroSection";
import Features from "./components/Features";
import StepGuide from "./components/StepGuide";
import Checklist from "./components/Checklist";
import Footer from "./components/Footer";
import LoanBuddy from "./components/LoanBuddy";
import LoanEligibilityChecker from "./components/LoanEligibilityChecker";
import LoanDisplay from "./components/LoanDisplay";
import agriLoans from './files/agri_lending.json';
import msmeLoans from './files/msme.json';
import ChatInterface from "./components/ChatInterface";
import DocumentUpload from "./components/DocumentUpload";
import TransactionAnalysis from "./components/TransactionAnalysis";
import UserForm from "./components/UserForm";
import Dashboard from "./components/Dashboard";

const App = () => {
  // Combine both loan arrays
  const allLoans = [...agriLoans, ...msmeLoans];

  return (
    <Router>
      <div>
        <Navbar />
        <Routes>
          <Route path="/" element={<><HeroSection /><Features /></>} />
          <Route path="/guide" element={<StepGuide />} />
          <Route path="/ai-companion" element={<LoanBuddy />} />
          <Route path="/checklist" element={<Checklist />} />
          <Route path="/loans" element={<LoanDisplay loans={allLoans} />} />
          <Route path="/eligibility" element={<LoanEligibilityChecker agriLoans={agriLoans} msmeLoans={msmeLoans} />} />
          <Route path="/chat" element={<ChatInterface />} />
          <Route path="/upload" element={<DocumentUpload />} />
          <Route path="/analysis" element={<TransactionAnalysis />} />
          <Route path="/startform" element={<UserForm />} />
          <Route path="/dashboard" element={<Dashboard />} />

        </Routes>
        <Footer />
      </div>
    </Router>
  );
};

export default App;
