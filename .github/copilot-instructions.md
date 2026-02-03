# Copilot Instructions for BachtrackAPI

## Project Overview
BachtrackAPI is a web scraper and REST API for the Bachtrack classical music events database. It extracts opera event listings by work ID, including city, venue, dates, and detailed information. The project consists of two main parts:
- **Scraper**: Extracts event data from Bachtrack HTML pages
- **FastAPI Backend**: RESTful API exposing search functionality

## Architecture

### Folder Structure
```
scrapers/
  └── bachtrack/
      └── scraper.py          # Core scraping logic (BachtrackScraper class)
api/
  ├── main.py                 # FastAPI app factory
  ├── routes/
  │   └── events.py          # Event search endpoints
  ├── models/
  │   └── event.py           # Pydantic models (OperaEvent, SearchRequest, etc)
  └── services/
      └── opera_service.py    # Service layer bridging scraper & API
tests/
  (placeholder for unit tests)
```

### Key Components

#### 1. Scraper (`scrapers/bachtrack/scraper.py`)
- `BachtrackScraper` class handles all web scraping
- `search_operas(search_input)` - searches by either:
  - Bachtrack work ID (int): `search_operas(12285)` → `https://bachtrack.com/search-opera/work=12285`
  - Freetext search (str): `search_operas("La Traviata")` → `https://bachtrack.com/search-opera/freetext=La%20Traviata`
- Returns list of dicts with: `title`, `city`, `dates` (list), `venue`, `detail_url`
- `get_event_details(detail_url)` - fetches address and metadata from event detail pages
- Robust error handling and HTML parsing with BeautifulSoup

#### 2. Data Models (`api/models/event.py`)
- `OperaEvent` - core event structure (title, city, dates list, venue, detail_url)
- `SearchRequest` - POST request body with work_id
- `SearchResponse` - API response with work_id, total_results, results array

#### 3. API Routes (`api/routes/events.py`)
- `GET /api/v1/events/search?work_id=12285` - search by work ID
- `GET /api/v1/events/search?q=Carmen` - freetext search
- `POST /api/v1/events/search` - JSON body search with either `work_id` or `search_term`
- All return `SearchResponse` with query, total_results, and events array
- Validation: Must provide either work_id OR q/search_term, not both

#### 4. Service Layer (`api/services/opera_service.py`)
- `OperaEventService` - orchestrates scraper and model conversion
- `search_operas_by_work_id()` - converts raw dict data to Pydantic models

### Data Flow
1. Client requests `/api/v1/events/search?work_id=12285` OR `/api/v1/events/search?q=Carmen`
2. Route handler calls `OperaEventService.search_operas(search_input)`
3. Service calls `BachtrackScraper.search_operas(search_input)`
4. Scraper constructs appropriate URL:
   - Work ID: `https://bachtrack.com/search-opera/work=12285`
   - Freetext: `https://bachtrack.com/search-opera/freetext=Carmen` (URL-encoded)
5. Scraper parses `<li data-type='nothing'>` elements for:
   - City: `<div class="listing-ms-city">`
   - Venue: `<div class="listing-ms-venue">`
   - Dates: `<div class="listing-ms-dates">` (comma-separated, parsed to list)
   - Title: `<div class="listing-ms-main">` (with "Wish list" text removed)
   - Detail URL: `<a class="listing-ms-right">` href attribute
6. Service converts to `OperaEvent` objects and returns in `SearchResponse`

## Development Conventions

### Web Scraping Patterns
- Work ID URL: `https://bachtrack.com/search-opera/work={work_id}`
- Freetext URL: `https://bachtrack.com/search-opera/freetext={encoded_search}`
- Always use custom User-Agent header to avoid 403 errors
- Always URL-encode freetext searches (handled by `urllib.parse.quote()`)
- Target CSS classes:
  - `listing-ms-city` - city name
  - `listing-ms-venue` - theater/venue name
  - `listing-ms-dates` - comma-separated dates (may include qualifiers like "10 mat", "Sun 3 May at 14:00")
  - `listing-ms-main` - title (contains "Wish list" button text that must be stripped)
- Date format: "Apr 05, 10, 15, 17" (abbreviation + day numbers)
- Address extraction: `<span class="listing-address">` from detail pages

### Code Organization
- **scrapers/**: Pure data extraction (no API knowledge)
- **api/models/**: Pydantic validation schemas
- **api/routes/**: FastAPI endpoint definitions (thin layer)
- **api/services/**: Business logic, scraper orchestration
- **test_scraper.py**: Standalone scraper testing script
- **test_api.py**: Full integration testing script

### Testing
Run `python test_scraper.py` to verify scraper extracts City, Theater, Dates correctly.
Run `python test_api.py` to verify full API integration (both GET/POST endpoints).

## External Dependencies
- `fastapi==0.104.1` - async web framework
- `uvicorn[standard]==0.24.0` - ASGI server
- `pydantic==2.5.0` - data validation
- `requests==2.31.0` - HTTP client
- `beautifulsoup4==4.12.2` - HTML parsing
- `selenium==4.15.2` - dynamic rendering (for future JS-heavy pages)
- `webdriver-manager==4.0.1` - auto-manage ChromeDriver

## Running the Project

```bash
# Install dependencies
pip install -r requirements.txt

# Run scraper test (verify Gianni Schicchi extraction)
python test_scraper.py

# Run API integration test
python test_api.py

# Start server
uvicorn api.main:app --reload

# Access interactive docs
# GET http://localhost:8000/docs
# GET http://localhost:8000/redoc
```

## Key Examples
- Work ID 12285: Gianni Schicchi - Puccini (6 events found in test)
- URL pattern for search: `https://bachtrack.com/search-opera/work=12285`
- API request: `GET /api/v1/events/search?work_id=12285`
- Response includes 6 events across Berlin, Winterthur, NYC, Vilnius, Vienna, Budapest
