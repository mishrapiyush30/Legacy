import React, { useState } from 'react';

/**
 * Component to display a case card with highlights.
 * 
 * @param {Object} props - Component props
 * @param {Object} props.case - Case object
 * @param {Function} props.onSelect - Function to call when case is selected
 * @param {boolean} props.isSelected - Whether the case is selected
 * @returns {JSX.Element} Case card component
 */
const CaseCard = ({ case: caseItem, onSelect, isSelected }) => {
  const { case_id, context, response, score } = caseItem;
  const [showFullResponse, setShowFullResponse] = useState(false);
  
  return (
    <div 
      className={`border rounded-lg p-4 mb-4 bg-white shadow-sm ${isSelected ? 'border-teal-500 bg-teal-50' : 'border-gray-200'}`}
    >
      <div className="flex justify-between items-center mb-2">
        <h3 className="text-lg font-semibold text-gray-800">Conversation #{case_id}</h3>
        <div className="flex items-center">
          <input 
            type="checkbox" 
            checked={isSelected} 
            onChange={() => onSelect(caseItem)}
            className="w-4 h-4 text-teal-600 rounded focus:ring-teal-500"
          />
        </div>
      </div>
      
      <div className="mb-3">
        <h4 className="text-sm font-medium text-gray-700 mb-1">Context:</h4>
        <p className="text-sm text-gray-800 bg-gray-50 p-3 rounded">{context}</p>
      </div>
      
      <div className="mb-3">
        <div className="flex justify-between items-center">
          <h4 className="text-sm font-medium text-gray-700 mb-1">
            {showFullResponse ? "Full Response:" : "Summary:"}
          </h4>
          <div className="flex space-x-2">
            <button 
              onClick={() => setShowFullResponse(!showFullResponse)}
              className="text-xs text-teal-600 hover:text-teal-800"
            >
              {showFullResponse ? 'Hide Full Response' : 'Show Full Response'}
            </button>
          </div>
        </div>
        
        {showFullResponse ? (
          <div className="bg-teal-50 p-3 rounded text-sm mb-2">
            <p className="text-gray-800">{response}</p>
          </div>
        ) : (
          <div className="bg-gray-50 p-3 rounded text-sm mb-2">
            <p className="text-gray-800">{response.length > 150 ? response.substring(0, 150) + "..." : response}</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default CaseCard; 