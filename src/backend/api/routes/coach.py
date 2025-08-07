import logging
import asyncio
from typing import Dict, Any, List
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel

from api.dependencies import get_services
from api.middleware import metrics
from api.config import config

logger = logging.getLogger(__name__)

router = APIRouter()

class CoachRequest(BaseModel):
    """Request body for coach endpoint."""
    query: str
    case_ids: List[int] = []  # Optional list of selected case IDs

@router.post("/api/coach")
async def coach(
    request: CoachRequest,
    services: Dict[str, Any] = Depends(get_services)
):
    """Generate coaching response."""
    logger.info(f"Coach request: {request.query}")
    
    try:
        # Get services
        retrieval_service = services["retrieval_service"]
        coach_service = services["coach_service"]
        
        # Get cases
        if request.case_ids and len(request.case_ids) > 0:
            logger.info(f"Using selected case IDs: {request.case_ids}")
            # Get cases from selected IDs
            cases = []
            for case_id in request.case_ids:
                case_results = retrieval_service.search_cases(
                    request.query, 
                    filter_case_ids=[case_id],
                    include_highlights=False
                )
                if case_results:
                    cases.extend([{
                        "case_id": c.case_id,
                        "context": c.context,
                        "response": c.response
                    } for c in case_results])
        else:
            # Search for relevant cases
            search_results = retrieval_service.search_cases(
                request.query,
                include_highlights=False
            )
            
            # Convert to dict for coach service
            cases = [{
                "case_id": c.case_id,
                "context": c.context,
                "response": c.response
            } for c in search_results]
        
        # Generate coaching response with timeout
        response = await asyncio.wait_for(
            coach_service.coach(request.query, cases),
            timeout=config["coach_timeout"]
        )
        
        # Update gate metrics
        metrics["coach_requests"] += 1
        if getattr(response, "refused", False):
            metrics["gate_failed"] += 1
        else:
            metrics["gate_passed"] += 1
        
        return response.dict()
    except Exception as e:
        logger.exception(f"Error in coach endpoint: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}") 