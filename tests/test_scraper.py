"""Test script for Bachtrack scraper."""
import sys
from scraper.scraper import BachtrackScraper


def test_gianni_schicchi():
    """Test scraping Gianni Schicchi opera events."""
    scraper = BachtrackScraper()
    
    print("=" * 60)
    print("Testing Gianni Schicchi Scraping (Work ID: 12285)")
    print("=" * 60)
    
    try:
        # Search for Gianni Schicchi using work ID
        events = scraper.search_operas(12285)
        
        print(f"\n✓ Found {len(events)} events for Gianni Schicchi")
        print()
        
        if events:
            for i, event in enumerate(events, 1):
                print(f"Event {i}:")
                print(f"  Title:    {event.get('title')}")
                print(f"  City:     {event.get('city')}")
                print(f"  Venue:    {event.get('venue')}")
                print(f"  Dates:    {event.get('dates')}")
                print(f"  URL:      {event.get('detail_url')}")
                
                # If we have a detail URL, fetch more info
                if event.get('detail_url'):
                    print("  Fetching details...")
                    try:
                        details = scraper.get_event_details(event['detail_url'])
                        if details:
                            print(f"    Address: {details.get('address', 'N/A')}")
                            for key, value in details.items():
                                if key != 'address':
                                    print(f"    {key}: {value}")
                    except Exception as e:
                        print(f"    Error fetching details: {e}")
                
                print()
        else:
            print("No events found!")
            
    except Exception as e:
        print(f"✗ Error during scraping: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    
    print("=" * 60)
    print("Test completed successfully!")
    print("=" * 60)


if __name__ == "__main__":
    test_gianni_schicchi()
