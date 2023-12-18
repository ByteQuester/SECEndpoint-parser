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
import pandas as pd

from apps.functions.managers import LoggingManager
from apps.types import BASE_URL
from apps.utils import Roster


class SECAPIClient:
    def __init__(self, base_url=None):
        """
        Initialize the SECAPIClient with an optional base URL.
        If no base URL is provided, the default URL from SECEndpoints is used.
        """
        self.base_url = base_url if base_url else BASE_URL
        self.error_handler = LoggingManager()
        self.rate_limit = None
        self.cache = TTLCache(maxsize=100, ttl=3600)  # Cache for 1 hour
        self.roster = Roster()

    def fetch_company_tickers(self):
        """
        Fetch company tickers from the SEC API.
        Returns:
            pd.DataFrame or dict: The response from the API as a DataFrame, or a dict in case of error.
        """
        key = 'company_tickers'
        cached_response = self._get_from_cache(key)
        if cached_response:
            # If cached data is found, parse it and return
            return self._parse_response(cached_response, 'tickers')

        url = self.roster.api_endpoints["company_tickers"]
        response = self._send_get_request(url)
        if response:
            # Store the raw response in the cache instead of the parsed data
            self._store_in_cache(key, response, expiry=3600)  # Cache for 1 hour

            # Parse the response and return
            parsed_data = self._parse_response(response, 'tickers')
            if isinstance(parsed_data, pd.DataFrame):
                return parsed_data
            else:
                return {'error': 'Failed to parse company tickers'}

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
            self._store_in_cache(key, response, expiry=3600)  # Cache for 1 hour

            parsed_data = self._parse_response(response, 'submissions')
            if isinstance(parsed_data, pd.DataFrame):
                return parsed_data
            else:
                return {'error': 'Failed to parse company submissions'}

    def fetch_company_facts(self, cik_number):
        """
        Fetch company facts from the SEC API.
        Args:
            cik_number (str): The CIK number of the company.
        Returns:
            pd.DataFrame or dict: The response from the API as a DataFrame, or a dict in case of error.
        """
        key = f'company_facts_{cik_number}'
        cached_response = self._get_from_cache(key)
        if cached_response:
            # Parse the cached response and return
            return self._parse_response(cached_response, 'company_facts')

        url = self.roster.recruit_cik(cik_number).api_endpoints["company_facts"]
        response = self._send_get_request(url)
        if response:
            # Cache the raw response for future use
            self._store_in_cache(key, response, expiry=3600)  # Cache for 1 hour

            # Parse the response and return
            parsed_data = self._parse_response(response, 'company_facts')
            if isinstance(parsed_data, pd.DataFrame):
                return parsed_data
            else:
                return {'error': 'Failed to parse company facts'}

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
            pd.DataFrame or None: The parsed response as a DataFrame, or None in case of error.
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
                all_flattened_data = []

                for metric_key, metric_data in response['facts']['us-gaap'].items():
                    if 'units' in metric_data and 'USD' in metric_data['units']:
                        usd_data = metric_data['units']['USD']

                        flattened_data = [
                            {
                                'EntityName': entityname,
                                'CIK': cik,
                                'Metric': metric_key,
                                **item  # Spread the individual item fields
                            }
                            for item in usd_data
                        ]
                        all_flattened_data.extend(flattened_data)

                return pd.DataFrame(all_flattened_data)
            else:
                self.error_handler.log_error(f"Unknown response type: {response_type}")
                return None
        except Exception as e:
            self.error_handler.log_error(f"Error parsing response: {str(e)}")
            return None

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