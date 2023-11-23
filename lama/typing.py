from enum import Enum


class SECEndpoints(Enum):
    BASE_URL = "https://data.sec.gov"
    COMPANY_TICKERS = "/files/company_tickers.json"
    SUBMISSIONS = "/submissions/CIK{}.json"
    COMPANY_FACTS = "/api/xbrl/companyfacts/CIK{}.json"

    def full_url(self):
        return f'{self.BASE_URL.value}{self.value}'


# Usage example
# full_url = SECEndpoints.COMPANY_TICKERS.full_url()
