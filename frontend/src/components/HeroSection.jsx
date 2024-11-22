import React, { useEffect, useRef } from "react";
import { gsap } from "gsap";
import { useNavigate } from "react-router-dom";

const HeroSection = () => {
  const mapRef = useRef(null);
  const navRef = useRef(null);
  const navigate = useNavigate(); 
  return (
    <div className="bg-gradient-to-r from-blue-600 to-blue-800 py-24">
      <div className="container mx-auto text-center px-4">
        <h1 className="text-5xl font-extrabold text-white mb-6 leading-tight">
          Your Dream Loan <span className="text-yellow-400">Made Simple.</span>
        </h1>
        <p className="text-xl text-blue-100 mb-8 max-w-2xl mx-auto">
          India's first AI-powered loan companion that helps you get the perfect loan. Smart documentation, instant approval readiness, and personalized banking recommendations tailored just for you.
        </p>
        
        {/* Map section remains the same - represents nationwide bank coverage */}
        <div className="Container max-w-4xl mx-auto mb-12">
          {/* Previous map SVG content remains the same */}
        </div>

        <div className="space-x-4">
        <button 
        onClick={() => navigate('/chat')}
        className="bg-yellow-400 text-blue-900 px-8 py-3 rounded-full font-bold hover:bg-yellow-300 transition duration-300"
      >
        Get Your Loan Report
      </button>

          <button className="border-2 border-white text-white px-8 py-3 rounded-full font-bold hover:bg-white hover:text-blue-800 transition duration-300">
            View Success Stories
          </button>
        </div>

        <div className="mt-8 grid grid-cols-3 gap-4 max-w-3xl mx-auto text-white">
          <div className="p-4">
            <h3 className="font-bold text-xl mb-2">Smart Documentation</h3>
            <p>AI-generated perfect loan applications for any bank</p>
          </div>
          <div className="p-4">
            <h3 className="font-bold text-xl mb-2">Bank Matching</h3>
            <p>Find banks most likely to approve your loan</p>
          </div>
          <div className="p-4">
            <h3 className="font-bold text-xl mb-2">Credit Optimization</h3>
            <p>AI tips to improve your loan worthiness</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default HeroSection;
