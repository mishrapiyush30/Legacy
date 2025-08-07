import { useState, useEffect } from 'react';
import { API_BASE_URL } from '../config';

export const useAppState = () => {
  // State
  const [searchQuery, setSearchQuery] = useState('');
  const [searchResults, setSearchResults] = useState([]);
  const [selectedCases, setSelectedCases] = useState([]);
  const [isSearching, setIsSearching] = useState(false);
  const [isCoaching, setIsCoaching] = useState(false);
  const [coachResponse, setCoachResponse] = useState(null);
  const [error, setError] = useState(null);
  
  // Handle search
  const handleSearch = async (query) => {
    setSearchQuery(query);
    setIsSearching(true);
    setError(null);
    setCoachResponse(null);
    
    try {
      const response = await fetch(`${API_BASE_URL}/api/search_cases`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          query
        }),
      });
      
      if (!response.ok) {
        throw new Error(`Search failed: ${response.status}`);
      }
      
      const results = await response.json();
      // Sort results by relevance score (highest first)
      const sortedResults = results.sort((a, b) => b.score - a.score);
      setSearchResults(sortedResults);
      setSelectedCases([]);
    } catch (err) {
      console.error('Error searching cases:', err);
      setError(`Failed to search cases: ${err.message}`);
    } finally {
      setIsSearching(false);
    }
  };
  
  // Handle case selection
  const toggleCaseSelection = (caseItem) => {
    const caseId = caseItem.case_id;
    setSelectedCases(prevSelected => {
      if (prevSelected.includes(caseId)) {
        return prevSelected.filter(id => id !== caseId);
      } else {
        return [...prevSelected, caseId];
      }
    });
  };
  
  // Handle coaching
  const handleCoach = async () => {
    setIsCoaching(true);
    setCoachResponse(null);
    setError(null);

    try {
      // Get selected case IDs
      const selectedCaseIds = searchResults
        .filter(result => selectedCases.includes(result.case_id))
        .map(result => result.case_id);

      // Make sure we have at least one selected case
      if (selectedCaseIds.length === 0 && searchResults.length > 0) {
        // If no cases selected, use the first search result
        selectedCaseIds.push(searchResults[0].case_id);
      }

      console.log("Selected case IDs:", selectedCaseIds);

      const response = await fetch(`${API_BASE_URL}/api/coach`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          query: searchQuery,
          case_ids: selectedCaseIds
        }),
      });

      if (!response.ok) {
        throw new Error(`Coach API error: ${response.status}`);
      }

      const data = await response.json();
      setCoachResponse(data);
    } catch (err) {
      console.error('Error coaching:', err);
      setError(`Failed to get coaching response: ${err.message}`);
    } finally {
      setIsCoaching(false);
    }
  };

  return {
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
  };
}; 