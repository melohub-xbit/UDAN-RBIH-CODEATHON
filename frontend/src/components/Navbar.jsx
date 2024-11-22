import React from "react";
import { Link } from "react-router-dom";

const Navbar = () => {
  return (
    <nav className="bg-blue-600 text-white p-4">
      <div className="container mx-auto flex justify-between">
        <h1 className="text-xl font-bold">LoanBuddy AI</h1>
        <div className="space-x-4">
          <Link to="/">Home</Link>
          <Link to="/loan-guide">Loan Guide</Link>
          <Link to="/eligibility">Check Eligibility</Link>
          <Link to="/documents">Smart Documents</Link>
          <Link to="/ai-advisor">AI Advisor</Link>
          <Link to="/bank-match">Bank Matcher</Link>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
