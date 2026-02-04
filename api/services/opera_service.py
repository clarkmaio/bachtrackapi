"""Service layer for opera events business logic."""
from typing import List, Union
from scraper.scraper import BachtrackScraper
from api.models.event import OperaEvent, OperaEventDetail


class OperaEventService:
    """Service for opera event operations."""
    
    def __init__(self):
        self.scraper = BachtrackScraper()
    
    def search_operas(self, search_input: Union[int, str]) -> List[OperaEvent]:
        """
        Search for opera events by work ID or freetext search.
        
        Args:
            search_input: Either an integer work ID or a string search term
            
        Returns:
            List of OperaEvent objects
        """
        events = self.scraper.search_operas(search_input)
        return [OperaEvent(**event) for event in events]
    
    def get_event_details(self, detail_url: str) -> dict:
        """
        Get detailed information for an event.
        
        Args:
            detail_url: URL to event detail page
            
        Returns:
            Dictionary with additional details (address, etc)
        """
        return self.scraper.get_event_details(detail_url)
