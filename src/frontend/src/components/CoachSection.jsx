import React from 'react';
import CoachPanel from './CoachPanel';

const CoachSection = ({ 
  response, 
  isLoading, 
  onCoach, 
  hasSearchResults 
}) => {
  return (
    <div>
      <CoachPanel 
        response={response}
        isLoading={isLoading}
        onCoach={onCoach}
        hasSearchResults={hasSearchResults}
      />
    </div>
  );
};

export default CoachSection; 