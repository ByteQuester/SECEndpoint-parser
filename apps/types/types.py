from enum import Enum


class SECEndpoints(Enum):
    BASE_URL = "https://data.sec.gov"
    COMPANY_TICKERS = "/files/company_tickers.json"
    SUBMISSIONS = "/submissions/CIK{}.json"
    COMPANY_FACTS = "/api/xbrl/companyfacts/CIK{}.json"

    def full_url(self):
        # Handle the special case for COMPANY_TICKERS
        if self == SECEndpoints.COMPANY_TICKERS:
            return "https://www.sec.gov" + self.value
        return f'{self.BASE_URL.value}{self.value}'

