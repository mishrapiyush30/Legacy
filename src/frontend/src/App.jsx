import React from 'react';
import Layout from './components/Layout';
import SearchSection from './components/SearchSection';
import CoachSection from './components/CoachSection';
import { useAppState } from './hooks/useAppState';

/**
 * Main application component.
 * Purely component composition - no layout or styling.
 * All business logic is handled by the useAppState hook.
 * All layout is handled by Layout component.
 * 
 * @returns {JSX.Element} App component
 */
const App = () => {
  const {
    // State
    searchQuery,
    searchResults,
    selectedCases,
    isSearching,
    isCoaching,
    coachResponse,
    error,
    
    // Actions
    setSearchQuery,
    handleSearch,
    toggleCaseSelection,
    handleCoach
  } = useAppState();
  
  return (
    <Layout>
      <SearchSection 
        searchQuery={searchQuery}
        onQueryChange={setSearchQuery}
        onSearch={handleSearch}
        isSearching={isSearching}
        error={error}
        searchResults={searchResults}
        selectedCases={selectedCases}
        onCaseSelect={toggleCaseSelection}
      />
      
      <CoachSection 
        response={coachResponse}
        isLoading={isCoaching}
        onCoach={handleCoach}
        hasSearchResults={searchResults.length > 0}
      />
    </Layout>
  );
};

export default App; 