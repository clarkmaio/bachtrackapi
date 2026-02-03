"""Integration test for the full API."""
import asyncio
from api.main import app
from fastapi.testclient import TestClient


def test_api_integration():
    """Test the full API integration."""
    client = TestClient(app)
    
    print("=" * 60)
    print("Testing API Integration")
    print("=" * 60)
    
    # Test health check
    print("\n1. Testing health check endpoint...")
    response = client.get("/health")
    assert response.status_code == 200
    print(f"   ✓ Health check: {response.json()}")
    
    # Test GET search
    print("\n2. Testing GET /api/v1/events/search?work_id=12285...")
    response = client.get("/api/v1/events/search?work_id=12285")
    print(f"   Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"   ✓ Found {data['total_results']} events")
        print(f"   Query: {data['query']}")
        
        if data['results']:
            print(f"\n   First event:")
            event = data['results'][0]
            print(f"     Title:  {event['title']}")
            print(f"     City:   {event['city']}")
            print(f"     Venue:  {event['venue']}")
    else:
        print(f"   ✗ Error: {response.text}")
    
    # Test POST search
    print("\n3. Testing POST /api/v1/events/search...")
    response = client.post("/api/v1/events/search", json={"work_id": 12285})
    print(f"   Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"   ✓ Found {data['total_results']} events")
    else:
        print(f"   ✗ Error: {response.text}")
    
    # Test get_operas endpoint with freetext search
    print("\n4. Testing GET /api/v1/events/get_operas?q=gianni%20schicchi...")
    response = client.get("/api/v1/events/get_operas?q=gianni%20schicchi")
    print(f"   Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"   ✓ Raw scraper output: {len(data)} events found")
        
        if data:
            print(f"\n   First event structure:")
            event = data[0]
            for key, value in event.items():
                print(f"     {key}: {value}")
    else:
        print(f"   ✗ Error: {response.text}")
    
    # Test get_operas endpoint with work ID
    print("\n5. Testing GET /api/v1/events/get_operas?q=12285...")
    response = client.get("/api/v1/events/get_operas?q=12285")
    print(f"   Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"   ✓ Found {len(data)} events for work ID 12285")
        
        if data:
            print(f"\n   First event:")
            event = data[0]
            print(f"     Title: {event.get('title')}")
            print(f"     City:  {event.get('city')}")
            print(f"     Venue: {event.get('venue')}")
    else:
        print(f"   ✗ Error: {response.text}")
    
    # Test interactive API docs
    print("\n6. Testing OpenAPI docs...")
    response = client.get("/openapi.json")
    assert response.status_code == 200
    print(f"   ✓ OpenAPI schema available")
    
    print("\n" + "=" * 60)
    print("All tests passed!")
    print("=" * 60)


if __name__ == "__main__":
    test_api_integration()
