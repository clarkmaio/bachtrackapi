# BachtrackAPI

A Python web scraper and REST API for extracting classical music opera events from [Bachtrack.com](https://bachtrack.com/).

## Overview

BachtrackAPI provides two complementary ways to access opera event data:

1. **Scraper Module** - Direct web scraping of Bachtrack opera listings
2. **FastAPI Backend** - RESTful API endpoints for searching and filtering events

Search by work ID (e.g., `12285` for Gianni Schicchi) or freetext (e.g., `"La Traviata"`).

## Installation

```bash
pip install -r requirements.txt
```

## Quick Start

### 1. Using the Scraper Directly

```python
from scrapers.bachtrack.scraper import BachtrackScraper

scraper = BachtrackScraper()

# Search by work ID
events = scraper.search_operas(12285)  # Gianni Schicchi
print(f"Found {len(events)} events")

# Search by freetext
events = scraper.search_operas("La Traviata")
for event in events:
    print(f"{event['title']} - {event['city']} @ {event['venue']}")
```

**Output:**
```
Found 28 events
Gianni Schicchi - Berlin @ Deutsche Oper
Gianni Schicchi - Winterthur @ Stadttheater Winterthur
...
```

### 2. Using the FastAPI Backend

Start the server:
```bash
uvicorn api.main:app --reload
```

**Example API Requests:**

```bash
# Freetext search
curl "http://localhost:8000/api/v1/events/get_operas?q=gianni%20schicchi"

# Work ID search
curl "http://localhost:8000/api/v1/events/get_operas?q=12285"

# POST search
curl -X POST "http://localhost:8000/api/v1/events/search" \
  -H "Content-Type: application/json" \
  -d '{"work_id": 12285}'
```

**Response:**
```json
{
  "query": "12285",
  "total_results": 28,
  "results": [
    {
      "title": "Gianni Schicchi",
      "city": "Berlin",
      "date": "2026-04-05T00:00:00",
      "venue": "Deutsche Oper",
      "detail_url": "https://bachtrack.com/opera-event/..."
    }
  ]
}
```

## Available Endpoints

- `GET /api/v1/events/get_operas?q=<search>` - Raw scraper output
- `GET /api/v1/events/search?work_id=<id>` - Search by work ID
- `GET /api/v1/events/search?q=<term>` - Freetext search
- `POST /api/v1/events/search` - JSON body search
- `GET /docs` - Interactive API documentation
- `GET /health` - Health check

## Testing

```bash
# Run scraper tests
python tests/test_scraper.py

# Run full API integration tests
pytest tests/test_api.py -v -s
```

## Project Structure

```
scrapers/bachtrack/scraper.py    # Core scraping logic
api/
  ├── main.py                    # FastAPI app factory
  ├── routes/events.py           # API endpoints
  ├── models/event.py            # Pydantic models
  └── services/opera_service.py  # Service layer
tests/                           # Unit and integration tests
```

## License

MIT License - see [LICENSE](LICENSE) file for details

