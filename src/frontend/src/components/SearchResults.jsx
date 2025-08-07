import React from 'react';
import CaseCard from './CaseCard';

const SearchResults = ({ 
  isSearching, 
  error, 
  searchResults, 
  selectedCases, 
  onCaseSelect 
}) => {
  if (isSearching) {
    return (
      <div className="mt-8">
        <h2 className="text-lg font-semibold mb-4">Search Results</h2>
        <div className="flex justify-center items-center h-32 bg-white rounded-lg shadow-md">
          <div className="animate-spin rounded-full h-8 w-8 border-t-2 border-b-2 border-teal-500"></div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="mt-8">
        <h2 className="text-lg font-semibold mb-4">Search Results</h2>
        <div className="bg-red-50 border-l-4 border-red-400 p-4 rounded-lg shadow-md">
          <p className="text-red-700">{error}</p>
        </div>
      </div>
    );
  }

  if (searchResults.length === 0) {
    return (
      <div className="mt-8">
        <h2 className="text-lg font-semibold mb-4">Search Results</h2>
        <div className="text-center py-8 text-gray-500 bg-white rounded-lg shadow-md">
          <p>No results found</p>
        </div>
      </div>
    );
  }

  return (
    <div className="mt-8">
      <h2 className="text-lg font-semibold mb-4">Search Results</h2>
      <div className="space-y-4">
        {searchResults.map(result => (
          <CaseCard 
            key={result.case_id}
            case={result}
            onSelect={onCaseSelect}
            isSelected={selectedCases.includes(result.case_id)}
          />
        ))}
      </div>
    </div>
  );
};

export default SearchResults; 