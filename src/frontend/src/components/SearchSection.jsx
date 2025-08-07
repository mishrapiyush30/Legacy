import React from 'react';
import SearchPanel from './SearchPanel';
import SearchResults from './SearchResults';

const SearchSection = ({ 
  searchQuery, 
  onQueryChange, 
  onSearch, 
  isSearching, 
  error, 
  searchResults, 
  selectedCases, 
  onCaseSelect 
}) => {
  return (
    <div>
      <div className="bg-white rounded-lg shadow-md overflow-hidden">
        <div className="p-6">
          <SearchPanel 
            query={searchQuery}
            onQueryChange={onQueryChange}
            onSearch={onSearch}
            isLoading={isSearching}
          />
        </div>
      </div>
      
      <SearchResults 
        isSearching={isSearching}
        error={error}
        searchResults={searchResults}
        selectedCases={selectedCases}
        onCaseSelect={onCaseSelect}
      />
    </div>
  );
};

export default SearchSection; 