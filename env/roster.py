import requests

from lama.typing import SECEndpoints


class Roster:
    def __init__(self):
        self.cik = None
        self.api_endpoints = {
            "company_tickers": "https://www.sec.gov/files/company_tickers.json",  # Direct URL
            "submissions": SECEndpoints.SUBMISSIONS.full_url(),
            "company_facts": SECEndpoints.COMPANY_FACTS.full_url(),
        }
        self.api_status = {}
        self.headers = {'User-Agent': "your_email@example.com"}

    def recruit_cik(self, cik: str):
        self.cik = cik
        self._update_api_endpoints(cik)
        self.api_status = self._check_api_status()

    def _update_api_endpoints(self, cik):
        # Only update endpoints that require a CIK
        for key in ['submissions', 'company_facts']:
            self.api_endpoints[key] = self.api_endpoints[key].format(cik)

    def _check_api_status(self):
        status = {}
        for endpoint_name, endpoint_url in self.api_endpoints.items():
            try:
                response = requests.get(endpoint_url, headers=self.headers)
                status[endpoint_name] = 'OK' if response.status_code == 200 else f'Failed (Status Code: {response.status_code})'
            except Exception as e:
                status[endpoint_name] = f'Error: {str(e)}'
        return status

    def get_api_status(self):
        return self.api_status

    def print_cik(self):
        print("Current CIK: {}".format(self.cik))
