"""Test API with both search methods."""
import sys
from pathlib import Path

# Ensure the inner `bachtrackapi` package directory is on sys.path so
# `backend` imports resolve after the project restructure.
sys.path.insert(0, str(Path(__file__).parent.parent / "bachtrackapi"))

from backend.main import app
from fastapi.testclient import TestClient


def test_api_both_methods():
    """Test API with work_id and freetext search."""
    client = TestClient(app)
    
    print("=" * 70)
    print("Testing API - Both Search Methods")
    print("=" * 70)
    
    # Test GET with work_id
    print("\n1. GET /api/v1/events/search?work_id=12285")
    response = client.get("/api/v1/events/search?work_id=12285")
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    data = response.json()
    print(f"   ✓ Status: {response.status_code}")
    print(f"   ✓ Found {data['total_results']} events")
    print(f"   ✓ Query: {data['query']}")
    
    # Test GET with freetext
    print("\n2. GET /api/v1/events/search?q=La%20Traviata")
    response = client.get("/api/v1/events/search?q=La%20Traviata")
    assert response.status_code == 200
    data = response.json()
    print(f"   ✓ Status: {response.status_code}")
    print(f"   ✓ Found {data['total_results']} events")
    print(f"   ✓ Query: {data['query']}")
    if data['results']:
        print(f"   ✓ First result: {data['results'][0]['title']} - {data['results'][0]['city']}")
    
    # Test POST with work_id
    print("\n3. POST /api/v1/events/search with work_id")
    response = client.post("/api/v1/events/search", json={"work_id": 12285})
    assert response.status_code == 200
    data = response.json()
    print(f"   ✓ Status: {response.status_code}")
    print(f"   ✓ Found {data['total_results']} events")
    
    # Test POST with search_term
    print("\n4. POST /api/v1/events/search with search_term")
    response = client.post("/api/v1/events/search", json={"search_term": "Carmen"})
    assert response.status_code == 200
    data = response.json()
    print(f"   ✓ Status: {response.status_code}")
    print(f"   ✓ Found {data['total_results']} events")
    print(f"   ✓ Query: {data['query']}")
    if data['results']:
        print(f"   ✓ First result: {data['results'][0]['title']} - {data['results'][0]['city']}")
    
    # Test error case: neither work_id nor q provided
    print("\n5. Error case: GET without parameters")
    response = client.get("/api/v1/events/search")
    assert response.status_code == 400
    print(f"   ✓ Status: {response.status_code} (expected error)")
    print(f"   ✓ Error: {response.json()['detail']}")
    
    # Test error case: both parameters provided
    print("\n6. Error case: GET with both parameters")
    response = client.get("/api/v1/events/search?work_id=12285&q=Carmen")
    assert response.status_code == 400
    print(f"   ✓ Status: {response.status_code} (expected error)")
    print(f"   ✓ Error: {response.json()['detail']}")
    
    print("\n" + "=" * 70)
    print("✓ All API tests passed!")
    print("=" * 70)


if __name__ == "__main__":
    test_api_both_methods()
