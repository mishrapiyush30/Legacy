import React from 'react';

const Header = () => {
  return (
    <header className="bg-gradient-to-r from-teal-600 to-teal-500 text-white shadow-lg">
      <div className="max-w-7xl mx-auto py-8 px-4 sm:px-6 lg:px-8 text-center">
        <h1 className="text-4xl font-bold">
          Your Personal <span className="text-teal-200">Compass</span>
        </h1>
        <p className="mt-2 text-xl">Wellness Guide</p>
        <p className="mt-3 text-sm text-teal-100 max-w-2xl mx-auto">
          Find personalized guidance with our AI-powered platform. Search through thousands of real conversations and get expert responses tailored to your needs.
        </p>
      </div>
    </header>
  );
};

export default Header; 