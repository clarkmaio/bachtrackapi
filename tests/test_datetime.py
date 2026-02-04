"""Test scraper with datetime parsing and event expansion."""
import sys
from pathlib import Path

# Ensure imports resolve to the `bachtrackapi` package directory.
sys.path.insert(0, str(Path(__file__).parent.parent / "bachtrackapi"))

from scraper.scraper import BachtrackScraper


def test_datetime_parsing():
    """Test scraper with datetime parsing for Gianni Schicchi."""
    scraper = BachtrackScraper()
    
    print("=" * 80)
    print("Testing Gianni Schicchi with Datetime Parsing")
    print("=" * 80)
    
    try:
        # Search for Gianni Schicchi using freetext
        events = scraper.search_operas("gianni schicchi")
        
        print(f"\n✓ Found {len(events)} total events (after date expansion)")
        print()
        
        if events:
            # Group by city to show the expansion
            events_by_city = {}
            for event in events:
                city = event['city']
                if city not in events_by_city:
                    events_by_city[city] = []
                events_by_city[city].append(event)
            
            # Display results
            for city, city_events in sorted(events_by_city.items()):
                print(f"{city} ({len(city_events)} dates):")
                print(f"  Venue: {city_events[0]['venue']}")
                print(f"  Dates:")
                for event in city_events:
                    print(f"    - {event['date'].strftime('%Y-%m-%d')}")
                print()
        else:
            print("No events found!")
            
    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()
    
    print("=" * 80)


def test_work_id_parsing():
    """Test work ID search with datetime parsing."""
    scraper = BachtrackScraper()
    
    print("\n" + "=" * 80)
    print("Testing Work ID 12285 with Datetime Parsing")
    print("=" * 80)
    
    try:
        events = scraper.search_operas(12285)
        print(f"\n✓ Found {len(events)} total events (after date expansion)")
        print()
        
        if events:
            for i, event in enumerate(events[:5], 1):
                print(f"Event {i}:")
                print(f"  Title: {event['title']}")
                print(f"  City:  {event['city']}")
                print(f"  Venue: {event['venue']}")
                print(f"  Date:  {event['date'].strftime('%Y-%m-%d %H:%M:%S')}")
                print()
            
            if len(events) > 5:
                print(f"... and {len(events) - 5} more events")
                
    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()
    
    print("=" * 80)


if __name__ == "__main__":
    test_datetime_parsing()
    test_work_id_parsing()
