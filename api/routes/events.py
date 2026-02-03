"""Event search endpoints."""
from fastapi import APIRouter, HTTPException, Query
from typing import List, Dict, Any
from api.models.event import SearchRequest, SearchResponse, OperaEvent
from api.services.opera_service import OperaEventService
from scrapers.bachtrack.scraper import BachtrackScraper


router = APIRouter(prefix="/api/v1/events", tags=["events"])
service = OperaEventService()
scraper = BachtrackScraper()


@router.get("/search", response_model=SearchResponse)
async def search_operas_get(
    work_id: int = Query(None, gt=0, description="Bachtrack work ID"),
    q: str = Query(None, min_length=1, max_length=200, description="Freetext search term")
):
    """
    Search for opera events by work ID or freetext.
    
    Args:
        work_id: Bachtrack work ID (e.g., 12285 for Gianni Schicchi)
        q: Freetext search term (e.g., "Il barbiere di Siviglia")
        
    Returns:
        SearchResponse with matching opera events
        
    Note: Provide either work_id OR q, not both
    """
    if not work_id and not q:
        raise HTTPException(status_code=400, detail="Provide either work_id or q parameter")
    
    if work_id and q:
        raise HTTPException(status_code=400, detail="Provide either work_id or q, not both")
    
    search_input = work_id if work_id else q
    
    try:
        results = service.search_operas(search_input)
        return SearchResponse(
            query=str(search_input),
            total_results=len(results),
            results=results
        )
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/search", response_model=SearchResponse)
async def search_operas_post(request: SearchRequest):
    """
    Search for opera events by work ID or freetext (POST method).
    
    Args:
        request: SearchRequest with either work_id or search_term
        
    Returns:
        SearchResponse with matching opera events
    """
    if request.work_id is None and request.search_term is None:
        raise HTTPException(status_code=400, detail="Provide either work_id or search_term")
    
    if request.work_id is not None and request.search_term is not None:
        raise HTTPException(status_code=400, detail="Provide either work_id or search_term, not both")
    
    search_input = request.work_id if request.work_id else request.search_term
    
    try:
        results = service.search_operas(search_input)
        return SearchResponse(
            query=str(search_input),
            total_results=len(results),
            results=results
        )
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/get_operas", response_model=List[Dict[str, Any]])
async def get_operas(q: str = Query(..., min_length=1, max_length=200, description="Search term (work ID or freetext)")):
    """
    Get opera events directly from scraper.
    
    Args:
        q: Search input - can be a work ID (int) or freetext search term
        
    Returns:
        Raw list of opera events from BachtrackScraper
        
    Example:
        GET /api/v1/events/get_operas?q=gianni%20schicchi
        GET /api/v1/events/get_operas?q=12285
    """
    try:
        # Try to convert to int if it looks like a work ID
        try:
            search_input = int(q)
        except ValueError:
            search_input = q
        
        results = scraper.search_operas(search_input)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Scraper error: {str(e)}")
