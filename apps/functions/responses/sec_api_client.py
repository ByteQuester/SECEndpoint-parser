'''
This file contains the enhanced implementation of the SECAPIClient class.
# TODO: Implement advanced rate limiting strategy for SEC API limits.
# TODO: Complete parsing logic implementation for submissions data and ticker endpoint.
# TODO: Develop a caching mechanism for frequently accessed data -more advanced.
# TODO: Optimize request headers, making User-Agent dynamic or configurable.
# TODO: Create unit tests for all public methods.
# TODO: Expand documentation with detailed method descriptions and examples
'''
from cachetools import TTLCache
import requests
import time

from logging_manager import LoggingManager
from lama.typing import SECEndpoints
from roster import Roster


class SECAPIClient:
    def __init__(self, base_url=None):
        """
        Initialize the SECAPIClient with an optional base URL.
        If no base URL is provided, the default URL from SECEndpoints is used.
        """
        self.base_url = base_url if base_url else SECEndpoints.BASE_URL.value
        self.error_handler = LoggingManager()
        self.rate_limit = None
        self.cache = TTLCache(maxsize=100, ttl=3600)  # Cache for 1 hour
        self.roster = Roster()

    def fetch_company_tickers(self):
        """
        Fetch company tickers from the SEC API.
        Returns:
            dict: The response from the API.
        """
        key = 'company_tickers'
        cached_data = self._get_from_cache(key)
        if cached_data:
            return cached_data

        url = self.roster.api_endpoints["company_tickers"]
        response = self._send_get_request(url)
        if response:
            parsed_data = self._parse_response(response, 'tickers')
            if parsed_data:
                self._store_in_cache(key, parsed_data, expiry=3600)  # Cache for 1 hour
                return parsed_data
        return {'error': 'Failed to fetch company tickers'}

    def fetch_submissions(self, cik_number):
        """
        Fetch submissions from the SEC API.
        Args:
            cik_number (str): The CIK number of the company.
        Returns:
            dict: The response from the API.
        """
        key = f'submissions_{cik_number}'
        cached_data = self._get_from_cache(key)
        if cached_data:
            return cached_data
        url = self.roster.recruit_cik(cik_number).api_endpoints["submissions"]
        response = self._send_get_request(url)
        if response:
            parsed_data = self._parse_response(response, 'submissions')
            if parsed_data:
                self._store_in_cache(key, parsed_data, expiry=3600)  # Cache for 1 hour
                return parsed_data
        return {'error': 'Failed to fetch submissions'}

    def fetch_company_facts(self, cik_number):
        """
        Fetch company facts from the SEC API.
        Args:
            cik_number (str): The CIK number of the company.
        Returns:
            dict: The response from the API.
        """
        key = f'company_facts_{cik_number}'
        cached_data = self._get_from_cache(key)
        if cached_data:
            return cached_data
        url = self.roster.recruit_cik(cik_number).api_endpoints["company_facts"]
        response = self._send_get_request(url)
        if response:
            parsed_data = self._parse_response(response, 'company_facts')
            if parsed_data:
                self._store_in_cache(key, parsed_data, expiry=3600)  # Cache for 1 hour
                return parsed_data
        return {'error': 'Failed to fetch company facts'}

    def _send_get_request(self, url):
        """
        Send a GET request to the SEC API.
        Args:
            url (str): The URL of the API endpoint.
        Returns:
            dict or None: The response from the API as a JSON object, or None if there was a parsing error.
        """
        headers = {'User-Agent': 'YourName <your_email@example.com>'}
        try:
            if self.rate_limit and self.rate_limit['remaining'] == 0:
                cooldown_period = self.rate_limit['reset'] - time.time()
                if cooldown_period > 0:
                    time.sleep(cooldown_period + 1)  # Add an extra second to ensure the cooldown period has passed
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            if 'X-RateLimit-Remaining' in response.headers:
                self.rate_limit = {
                    'remaining': int(response.headers['X-RateLimit-Remaining']),
                    'reset': int(response.headers['X-RateLimit-Reset'])
                }
            return response.json()
        except requests.exceptions.RequestException as e:
            error_message = f"Error sending GET request: {str(e)}"
            self.error_handler.log_error(error_message)
            return {'error': error_message}
        except Exception as e:
            error_message = f"Error during API request: {str(e)}"
            self.error_handler.log_error(error_message)
            return {'error': error_message}

    def _parse_response(self, response, response_type):
        """
        Parse the raw JSON response based on the type of data.
        Args:
            response (dict): The raw JSON response from the SEC API.
            response_type (str): The type of data (e.g., 'tickers', 'submissions', 'company_facts').
        Returns:
            dict or None: The parsed response.
        """
        try:
            if response_type == 'tickers':
                # Specific parsing logic for tickers
                pass
            elif response_type == 'submissions':
                # Specific parsing logic for submissions
                pass
            elif response_type == 'company_facts':
                entityname, cik = response['entityName'], response['cik']
                parsed_data = {}
                for metric_key, metric_data in response['facts']['us-gaap'].items():
                    if 'units' in metric_data and 'USD' in metric_data['units']:
                        usd_data = metric_data['units']['USD']
                        parsed_data[metric_key] = [{'end': item['end'], 'val': item['val']} for item in usd_data]
                return {
                "EntityName": entityname,
                "CIK": cik,
                "ParsedData": parsed_data
            }
            else:
                error_message = f"Unknown response type: {response_type}"
                self.error_handler.log_error(error_message)
                return {'error': error_message}
        except Exception as e:
            error_message = f"Error parsing response: {str(e)}"
            self.error_handler.log_error(error_message)
            return {'error': error_message}

    def _get_from_cache(self, key):
        """
        Retrieve data from the cache if it exists and is not expired.
        Args:
            key (str): The key to retrieve data from the cache.
        Returns:
            dict or None: The cached data, or None if it does not exist or is expired.
        """
        if key in self.cache:
            cached_data = self.cache[key]
            if cached_data['expiry'] > time.time():
                return cached_data['data']
        return None

    def _store_in_cache(self, key, data, expiry):
        """
        Store the API response in the cache with a specified expiry duration.
        Args:
            key (str): The key to store the data in the cache.
            data (dict): The API response data to be stored.
            expiry (int): The expiry duration in seconds.
        """
        self.cache[key] = {
            'data': data,
            'expiry': time.time() + expiry
        }

    def _refresh_cache(self):
        """
        Refresh the stored data in the cache after the expiry period.
        """
        for key, cached_data in self.cache.items():
            if cached_data['expiry'] <= time.time():
                del self.cache[key]