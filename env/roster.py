import requests
from lama.typing import SECEndpoints


class Roster:
    def __init__(self):
        self.cik = None
        self.api_endpoints = {
            "company_tickers": SECEndpoints.COMPANY_TICKERS.full_url(),
            # Initially, submissions and company_facts are just path templates
            "submissions": SECEndpoints.SUBMISSIONS.value,
            "company_facts": SECEndpoints.COMPANY_FACTS.value,
        }
        self.api_status = {}
        self.headers = {'User-Agent': "your_email@example.com"}

    def recruit_cik(self, cik: str):
        self.cik = cik
        self._update_api_endpoints(cik)
        self.api_status = self._check_api_status()

    def _update_api_endpoints(self, cik):
        # Format submissions and company_facts endpoints with the CIK
        self.api_endpoints["submissions"] = SECEndpoints.SUBMISSIONS.full_url().format(cik)
        self.api_endpoints["company_facts"] = SECEndpoints.COMPANY_FACTS.full_url().format(cik)

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
