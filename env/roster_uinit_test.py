'''
This file contains the unit tests for the Roster class.
'''
import unittest
from unittest.mock import patch
from roster import Roster


class RosterTest(unittest.TestCase):
    def setUp(self):
        self.roster = Roster()

    def test_recruit_cik(self):
        cik = "1234567890"
        expected_endpoints = {
            "company_tickers": "https://www.sec.gov/files/company_tickers.json",
            "submissions": "https://data.sec.gov/submissions/CIK1234567890.json",
            "company_facts": "https://data.sec.gov/api/xbrl/companyfacts/CIK1234567890.json"
        }
        self.roster.recruit_cik(cik)
        self.assertEqual(self.roster.cik, cik)
        self.assertEqual(self.roster.api_endpoints, expected_endpoints)

    @patch('roster.requests.get')
    def test_check_api_status(self, mock_get):
        mock_response = mock_get.return_value
        mock_response.status_code = 200
        expected_status = {
            "company_tickers": "OK",
            "submissions": "OK",
            "company_facts": "OK"
        }
        self.roster.api_endpoints = {
            "company_tickers": "https://www.sec.gov/files/company_tickers.json",
            "submissions": "https://data.sec.gov/submissions/CIK1234567890.json",
            "company_facts": "https://data.sec.gov/api/xbrl/companyfacts/CIK1234567890.json"
        }
        status = self.roster._check_api_status()
        self.assertEqual(status, expected_status)


if __name__ == '__main__':
    unittest.main()