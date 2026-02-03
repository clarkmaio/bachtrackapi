"""Test freetext search functionality."""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from scrapers.bachtrack.scraper import BachtrackScraper


def test_freetext_search():
    """Test scraping with freetext search."""
    scraper = BachtrackScraper()
    
    print("=" * 70)
    print("Testing Freetext Search: 'Il barbiere di Siviglia'")
    print("=" * 70)
    
    try:
        # Search for Il barbiere di Siviglia using freetext
        events = scraper.search_operas("Il barbiere di Siviglia")
        
        print(f"\n✓ Found {len(events)} events for 'Il barbiere di Siviglia'")
        print()
        
        if events:
            for i, event in enumerate(events[:3], 1):  # Show first 3
                print(f"Event {i}:")
                print(f"  Title:    {event.get('title')}")
                print(f"  City:     {event.get('city')}")
                print(f"  Venue:    {event.get('venue')}")
                print(f"  Dates:    {event.get('dates')}")
                print(f"  URL:      {event.get('detail_url')}")
                print()
            
            if len(events) > 3:
                print(f"... and {len(events) - 3} more events")
        else:
            print("No events found!")
            
    except Exception as e:
        print(f"✗ Error during scraping: {e}")
        import traceback
        traceback.print_exc()
    
    print("=" * 70)


def test_work_id_search():
    """Test scraping with work ID (existing functionality)."""
    scraper = BachtrackScraper()
    
    print("\n" + "=" * 70)
    print("Testing Work ID Search: 12285 (Gianni Schicchi)")
    print("=" * 70)
    
    try:
        events = scraper.search_operas(12285)
        print(f"\n✓ Found {len(events)} events")
        if events:
            print(f"First event: {events[0].get('title')} - {events[0].get('city')}")
            
    except Exception as e:
        print(f"✗ Error: {e}")
    
    print("=" * 70)


if __name__ == "__main__":
    test_freetext_search()
    test_work_id_search()
