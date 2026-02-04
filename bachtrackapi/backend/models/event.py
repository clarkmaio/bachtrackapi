"""Data models for opera events API."""
from pydantic import BaseModel, Field, HttpUrl
from datetime import datetime
from typing import Optional


class OperaEvent(BaseModel):
    """Opera event listing."""
    title: str = Field(..., description="Opera title")
    city: str = Field(..., description="City where event is held")
    date: datetime = Field(..., description="Event date and time")
    venue: str = Field(..., description="Venue name")
    detail_url: Optional[HttpUrl] = Field(None, description="URL to event details page")
    
    class Config:
        json_schema_extra = {
            "example": {
                "title": "La Bohème",
                "city": "Berlin",
                "date": "2026-04-05T00:00:00",
                "venue": "Deutsche Oper Berlin",
                "detail_url": "https://bachtrack.com/opera-event/la-boheme-deutsche-oper-berlin/428220"
            }
        }


class OperaEventDetail(BaseModel):
    """Extended opera event with details."""
    title: str
    city: str
    date: datetime
    venue: str
    detail_url: Optional[str] = None
    address: Optional[str] = Field(None, description="Venue address")
    additional_info: Optional[dict] = Field(None, description="Additional metadata from detail page")


class SearchRequest(BaseModel):
    """Search request parameters."""
    work_id: Optional[int] = Field(None, description="Bachtrack work ID", gt=0)
    search_term: Optional[str] = Field(None, description="Freetext search term", min_length=1, max_length=200)
    
    class Config:
        json_schema_extra = {
            "examples": [
                {"work_id": 12285},
                {"search_term": "Il barbiere di Siviglia"}
            ]
        }


class SearchResponse(BaseModel):
    """Search response with results."""
    query: str = Field(..., description="Search query (work_id or search term)")
    total_results: int = Field(..., description="Number of results found")
    results: list[OperaEvent] = Field(..., description="List of opera events")
    
    class Config:
        json_schema_extra = {
            "example": {
                "query": "12285",
                "total_results": 6,
                "results": [
                    {
                        "title": "Gianni Schicchi",
                        "city": "Berlin",
                        "date": "2026-04-05T00:00:00",
                        "venue": "Deutsche Oper",
                        "detail_url": "https://bachtrack.com/opera-event/gianni-schicchi-deutsche-oper-berlin/428220"
                    }
                ]
            }
        }
