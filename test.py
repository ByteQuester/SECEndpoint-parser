from env.roster import Roster

roster = Roster()

# Test with a known CIK
test_cik = "0000012927"  # CIK for Berkshire Hathaway Inc., as an example

# Recruit the CIK and check API status
roster.recruit_cik(test_cik)
roster.print_cik()

# Get and print the API status
api_status = roster.get_api_status()
print("API Status for CIK:", test_cik)
for endpoint, status in api_status.items():
    print(f"  {endpoint}: {status}")
