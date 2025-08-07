import logging
from typing import Dict, Any
from fastapi import HTTPException, Depends

from services.index_manager import IndexManager
from services.embedding_service import EmbeddingService
from services.retrieval_service import RetrievalService
from services.safety_service import SafetyService
from services.coach_service import CoachService
from api.config import config

logger = logging.getLogger(__name__)

# Initialize services (keeping global for now to maintain compatibility)
index_manager = IndexManager({
    "index_dir": config["index_dir"],
    "cases_path": config["cases_path"],
})

async def get_services():
    """Get initialized services."""
    if not index_manager.is_initialized():
        logger.error("Services not initialized. Please ensure indices are loaded on startup.")
        raise HTTPException(status_code=503, detail="Services not initialized. Please restart the application or run /index endpoint first.")
    
    context_index, response_index, cases, embedding_service = index_manager.get_indices()
    
    safety_service = SafetyService()
    
    retrieval_service = RetrievalService(
        context_index=context_index,
        response_index=response_index,
        embedding_service=embedding_service,
        cases=cases
    )
    
    coach_service = CoachService(
        cases=cases,
        safety_service=safety_service,
        config={"llm_api_key": config["llm_api_key"]}
    )
    
    return {
        "retrieval_service": retrieval_service,
        "safety_service": safety_service,
        "coach_service": coach_service,
        "embedding_service": embedding_service,
        "cases": cases
    } 