"""Bachtrack.com scraper for opera events."""
from typing import List, Dict, Union
from datetime import datetime
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote
import re


class BachtrackScraper:
    """Scraper for Bachtrack opera events."""

    BASE_URL = "https://bachtrack.com"
    
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Language': 'en-US,en;q=0.9',
            'Referer': 'https://bachtrack.com/',
            'Upgrade-Insecure-Requests': '1',
            'Connection': 'keep-alive'
        }

    def search_operas(self, search_input: Union[int, str]) -> List[Dict]:
        """
        Search for opera events by work ID or freetext search.
        
        Args:
            search_input: Either an integer work ID (e.g., 12285) or a string search term (e.g., "Il barbiere di Siviglia")
            
        Returns:
            List of opera event dictionaries with city, date, venue, title
        """
        if isinstance(search_input, int):
            # Search by work ID
            search_url = f"{self.BASE_URL}/search-opera/work={search_input}"
        else:
            # Search by freetext
            encoded_search = quote(search_input)
            search_url = f"{self.BASE_URL}/search-opera/freetext={encoded_search}"
        
        try:
            response = requests.get(search_url, headers=self.headers, timeout=10)
            response.raise_for_status()
        except requests.RequestException as e:
            raise RuntimeError(f"Failed to fetch search results: {e}")

        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract opera events from listing
        events = []
        li_elements = soup.find_all('li', {'data-type': 'nothing'})
        
        for element in li_elements:
            try:
                event_list = self._parse_event_element(element)
                events.extend(event_list)
            except (AttributeError, ValueError) as e:
                # Skip malformed elements
                continue
        
        return events

    def _parse_event_element(self, element) -> List[Dict]:
        """
        Parse individual event element and expand to multiple events for each date.
        
        Args:
            element: BeautifulSoup element representing an event listing
            
        Returns:
            List of dictionaries with event details, one per date
        """
        try:
            city = element.find('div', {'class': 'listing-ms-city'}).text.strip()
            date_str = element.find('div', {'class': 'listing-ms-dates'}).text.strip()
            venue = element.find('div', {'class': 'listing-ms-venue'}).text.strip()
            
            # Extract title from listing-ms-main, removing Wish list button
            main_div = element.find('div', {'class': 'listing-ms-main'})
            title = main_div.text.strip()
            # Remove the wish list placeholder text
            title = title.replace('Wish list', '').strip()
            
            # Get detail page URL
            detail_link = element.find('a', {'class': 'listing-ms-right'})
            detail_url = None
            if detail_link and detail_link.get('href'):
                detail_url = f"{self.BASE_URL}{detail_link['href']}"
            
            # Parse dates and create one event per date
            parsed_dates = self._parse_dates_list(date_str)
            events = []
            
            for parsed_date in parsed_dates:
                events.append({
                    'title': title,
                    'city': city,
                    'date': parsed_date,
                    'venue': venue,
                    'detail_url': detail_url,
                })
            
            return events
        except (AttributeError, TypeError):
            return []

    def _parse_dates_list(self, date_str: str) -> List[datetime]:
        """
        Parse date string and return list of datetime objects.
        
        Handles formats like:
        - "Apr 05, 10, 15, 17" (same month, same year - inferred as current/next year)
        - "Sun 3 May at 14:00" (full date with time)
        - "Feb 05, 07, 11, 13, 15 mat, 17, 19, 21" (with qualifiers like 'mat')
        
        Args:
            date_str: Date string with comma-separated dates
            
        Returns:
            List of datetime objects
        """
        # Clean up the date string
        date_str = ' '.join(date_str.split())
        date_parts = [d.strip() for d in date_str.split(',')]
        
        parsed_dates = []
        month = None
        year = None
        
        for part in date_parts:
            try:
                # Try to parse full date format: "Sun 3 May at 14:00"
                if 'at' in part:
                    dt = self._parse_full_date(part)
                else:
                    # Try abbreviated format like "May 03" or just "03"
                    dt = self._parse_abbreviated_date(part, month, year)
                    
                if dt:
                    parsed_dates.append(dt)
                    # Remember the month and year for subsequent dates
                    month = dt.month
                    year = dt.year
            except (ValueError, AttributeError):
                # Skip dates that can't be parsed
                continue
        
        return parsed_dates
    
    def _parse_full_date(self, date_str: str) -> datetime:
        """
        Parse full date format: "Sun 3 May at 14:00" or "Sunday 03 November 2024"
        
        Args:
            date_str: Full date string
            
        Returns:
            Parsed datetime object
        """
        # Remove qualifiers and extra whitespace
        date_str = date_str.replace(' mat', '').replace(' at ', ' ').strip()
        
        # Try format with time: "Sun 3 May 14:00"
        try:
            dt = datetime.strptime(date_str, '%a %d %b %H:%M')
            # Add current year
            return dt.replace(year=datetime.now().year)
        except ValueError:
            pass
        
        # Try format with weekday and time but no leading zero on day: "Sun 3 May 14:00"
        try:
            # Handle single digit day
            parts = date_str.split()
            if len(parts) >= 3:
                day = int(parts[1])
                month_str = parts[2]
                time_str = parts[3] if len(parts) > 3 else "00:00"
                dt = datetime.strptime(f"{day} {month_str} {time_str}", '%d %b %H:%M')
                return dt.replace(year=datetime.now().year)
        except (ValueError, IndexError):
            pass
        
        # Try format: "Sunday 03 November 2024"
        try:
            return datetime.strptime(date_str, '%A %d %B %Y')
        except ValueError:
            pass
        
        # Try format: "Sun 3 May" (no year, no time)
        try:
            dt = datetime.strptime(date_str, '%a %d %b')
            # Use current year
            return dt.replace(year=datetime.now().year)
        except ValueError:
            pass
        
        # Try format: "3 May" (no weekday, no year, no time)
        try:
            dt = datetime.strptime(date_str, '%d %b')
            # Use current year
            return dt.replace(year=datetime.now().year)
        except ValueError:
            pass
        
        raise ValueError(f"Could not parse date: {date_str}")
    
    def _parse_abbreviated_date(self, date_str: str, prev_month: int = None, prev_year: int = None) -> datetime:
        """
        Parse abbreviated date format like "05" (day only) or "May 03" (month and day)
        
        Args:
            date_str: Abbreviated date string
            prev_month: Month from previous date (for inferring month of day-only dates)
            prev_year: Year from previous date (for inferring year)
            
        Returns:
            Parsed datetime object
        """
        date_str = date_str.replace(' mat', '').strip()
        
        # Try "May 05" format
        try:
            dt = datetime.strptime(date_str, '%b %d')
            return dt.replace(year=prev_year or datetime.now().year)
        except ValueError:
            pass
        
        # Try "May 5" format (no leading zero)
        try:
            dt = datetime.strptime(date_str, '%b %e').replace(day=int(date_str.split()[-1]))
            return dt.replace(year=prev_year or datetime.now().year)
        except (ValueError, IndexError):
            pass
        
        # Try "05" or "5" format (day only) - use previous month/year
        try:
            day = int(date_str)
            if prev_month and prev_year:
                return datetime(prev_year, prev_month, day)
            else:
                # Fallback to current month/year
                today = datetime.now()
                return datetime(today.year, today.month, day)
        except ValueError:
            pass
        
        raise ValueError(f"Could not parse abbreviated date: {date_str}")

    def _parse_date(self, date_str: str) -> datetime:
        """
        Parse date string format: "Sunday 03 November 2024" -> datetime object
        
        Args:
            date_str: Date string in format "Day DD Month YYYY"
            
        Returns:
            Parsed datetime object
        """
        # Handle multi-line date strings (strip extra whitespace)
        date_str = ' '.join(date_str.split())
        return datetime.strptime(date_str, '%A %d %B %Y')

    def get_event_details(self, detail_url: str) -> Dict:
        """
        Fetch additional event details from event detail page.
        
        Args:
            detail_url: URL of event detail page
            
        Returns:
            Dictionary with address and additional metadata
        """
        try:
            response = requests.get(detail_url, headers=self.headers, timeout=10)
            response.raise_for_status()
        except requests.RequestException as e:
            raise RuntimeError(f"Failed to fetch event details: {e}")

        soup = BeautifulSoup(response.content, 'html.parser')
        
        details = {}
        
        # Extract address
        address_span = soup.find('span', {'class': 'listing-address'})
        if address_span:
            details['address'] = address_span.text.strip()
        
        # Extract table data if present
        table_tbody = soup.find('tbody', {'class': 'plassmap_table'})
        if table_tbody:
            rows = table_tbody.find_all('tr')
            for row in rows:
                cells = row.find_all('td')
                if len(cells) >= 2:
                    key = cells[0].text.strip()
                    value = cells[1].text.strip()
                    details[key.lower()] = value
        
        return details
