import logging
import time
import asyncio
from typing import List, Dict, Any
from fastapi import APIRouter, HTTPException, Depends

from models.schema import SearchRequest, SearchResult
from api.dependencies import get_services
from api.config import config

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/api/search_cases", response_model=List[SearchResult])
async def search_cases(
    request: SearchRequest,
    services: Dict[str, Any] = Depends(get_services)
):
    """Search for cases similar to the query."""
    start_time = time.time()
    logger.info(f"Searching for cases: {request.query}")
    
    # Get services
    retrieval_service = services["retrieval_service"]
    
    # Set timeout
    try:
        # Search for cases
        results = await asyncio.wait_for(
            asyncio.to_thread(retrieval_service.search_cases, request.query, request.k, None, False),
            timeout=config["search_timeout"]
        )
        
        logger.info(f"Found {len(results)} cases in {time.time() - start_time:.2f}s")
        return results
    except asyncio.TimeoutError:
        logger.error(f"Search timed out after {config['search_timeout']}s")
        raise HTTPException(status_code=504, detail="Search timed out") 