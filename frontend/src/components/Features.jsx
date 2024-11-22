import React from "react";
import { FaRobot, FaFileAlt, FaChartLine, FaCheckCircle, FaUniversity, FaShieldAlt } from "react-icons/fa";

const Features = () => {
  const features = [
    {
      icon: <FaRobot className="w-8 h-8" />,
      title: "AI Loan Advisor",
      description: "Get personalized loan recommendations and instant eligibility checks powered by advanced AI"
    },
    {
      icon: <FaFileAlt className="w-8 h-8" />,
      title: "Smart Documentation",
      description: "Generate perfect loan applications with our AI document preparation system"
    },
    {
      icon: <FaChartLine className="w-8 h-8" />,
      title: "Credit Score Booster",
      description: "Receive AI-driven tips to improve your creditworthiness and loan approval chances"
    },
    {
      icon: <FaCheckCircle className="w-8 h-8" />,
      title: "Instant Eligibility",
      description: "Know your loan eligibility across multiple banks in seconds"
    },

  ];

  return (
    <div className="bg-gray-50 py-24">
      <div className="container mx-auto px-4">
        <h2 className="text-4xl font-bold text-center mb-16 text-gray-800">
          Smart Features for Your Loan Journey
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-1 lg:grid-cols-4 gap-8">
          {features.map((feature, index) => (
            <div key={index} className="bg-white p-8 rounded-xl shadow-lg hover:shadow-xl transition duration-300">
              <div className="text-blue-600 mb-4">{feature.icon}</div>
              <h3 className="text-xl font-bold mb-3 text-gray-800">{feature.title}</h3>
              <p className="text-gray-600">{feature.description}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default Features;
