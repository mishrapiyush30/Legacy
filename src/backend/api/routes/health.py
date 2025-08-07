import os
import logging
from typing import Dict, Any
from fastapi import APIRouter, HTTPException, Depends
from api.dependencies import index_manager, get_services
from api.config import config

logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/health")
async def health_check():
    """Health check endpoint."""
    # Check if pre-built indices exist (they should always exist in production)
    indices_exist = (
        os.path.exists(os.path.join(config["index_dir"], "index_manifest.json")) and
        os.path.exists(config["cases_path"])
    )
    
    # Show initialized=true if indices exist OR if manager is initialized
    is_ready = index_manager.is_initialized() or indices_exist
    
    return {"status": "ok", "initialized": is_ready}

@router.get("/api/cases/{case_id}")
async def get_case(
    case_id: int,
    services: Dict[str, Any] = Depends(get_services)
):
    """Get a specific case by ID."""
    cases = services["cases"]
    
    try:
        case = next(c for c in cases if c.id == case_id)
        return {
            "case_id": case.id,
            "context": case.context,
            "response": case.response,
            "response_sentences": [
                {
                    "sent_id": i,
                    "text": sentence.text,
                    "start": sentence.start,
                    "end": sentence.end
                }
                for i, sentence in enumerate(case.response_sentences)
            ]
        }
    except StopIteration:
        raise HTTPException(status_code=404, detail=f"Case {case_id} not found")
    except Exception as e:
        logger.error(f"Error getting case {case_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error") 