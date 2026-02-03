"""Inspect Bachtrack page structure."""
import requests
from bs4 import BeautifulSoup


def inspect_page():
    """Inspect the Gianni Schicchi work page."""
    url = 'https://bachtrack.com/search-opera/work=12285'
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    print(f"Fetching {url}...")
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Save HTML for inspection
    with open('/tmp/bachtrack_page.html', 'w', encoding='utf-8') as f:
        f.write(soup.prettify())
    
    print("✓ HTML saved to /tmp/bachtrack_page.html")
    
    # Look for event listings
    print("\n--- Looking for event containers ---")
    
    # Try different selectors
    li_elements = soup.find_all('li', {'data-type': 'nothing'})
    print(f"Found {len(li_elements)} <li data-type='nothing'> elements")
    
    # Look for divs with listing classes
    listings = soup.find_all('div', class_='listing-shortform')
    print(f"Found {len(listings)} .listing-shortform elements")
    
    # Check for all divs with 'listing' in class
    all_listings = soup.find_all(class_=lambda x: x and 'listing' in x)
    print(f"Found {len(all_listings)} elements with 'listing' in class")
    
    # Show first few elements
    if li_elements:
        print("\n--- First <li> element structure ---")
        print(li_elements[0].prettify()[:2000])
    
    if listings:
        print("\n--- First .listing-shortform element structure ---")
        print(listings[0].prettify()[:2000])


if __name__ == "__main__":
    inspect_page()
