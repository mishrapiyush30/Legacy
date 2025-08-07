from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class SentenceSpan(BaseModel):
    """Represents a sentence with its character offsets in the original text."""
    text: str
    start: int
    end: int


class CaseItem(BaseModel):
    """Represents a case from the counseling Q&A corpus."""
    id: int
    context: str
    response: str
    response_sentences: List[SentenceSpan] = Field(default_factory=list)


class SearchResult(BaseModel):
    """A case returned from search."""
    case_id: int
    context: str
    response: str  # Added full response
    score: float


class SearchRequest(BaseModel):
    """Request for case search."""
    query: str
    k: int = 3


class CoachRequest(BaseModel):
    """Request for coaching."""
    query: str
    case_ids: List[int]


class CoachResponse(BaseModel):
    """Response from the coach service."""
    answer_markdown: Optional[str] = None  # Full markdown response from synthesis
    citations: List[Dict[str, Any]] = []
    refused: bool = False
    refusal_reason: Optional[str] = None


class SynthesisOutput(BaseModel):
    """Output from the synthesis LLM call."""
    answer_markdown: str              # full final text, markdown allowed
    citations: List[Dict[str, Any]]  # case_id, sent_id 