import requests
import time

STREAMLABS_TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbiI6IjJGRUE4QjI2MjgxQkMzN0YxMzFDQjJDQjg1RUJDREU2NzIxNDdEQ0M1NjM2MDVCMUE2MEMxNjRCM0Y2QkFFRDk1MkI0NDMyNUVGRDkwNjYxMkIxN0I3RENBRDBFNjkxRTgxQTkyNTg4RTBFNzEzMEVCNTY4NEUwOEU3MzhDQzQ4OTc2NkM1M0I0REEzOTZGMzhDNkQ1RjYwMkYzNjE3MUQ1MkRDNkZCN0RCMEZCOEMyREIwQkNEOURFNzI0QzBFMzNBNUYyNzMxRTRCNTM5MTQzQzgyNDUxQzgwRDU1OERBMkUyMzZDOTYwMzFDNDA2REU3NzU1M0YxNkIiLCJyZWFkX29ubHkiOnRydWUsInByZXZlbnRfbWFzdGVyIjp0cnVlLCJmYWNlYm9va19pZCI6IjUyODU3MjU1ODQ3ODY0MDEiLCJzdHJlYW1sYWJzX2lkIjoiNzI3MDQ5MDk2NTI1NTY1MTMyOCJ9.prfUJ7sJOt79GCjWrYcUU53fO3sXG3gh3nHPRuGO_8w"


def send_streamlabs_alert(amount: float, battletag: str = "Anonymous", message: str = "New donation!"):
    """
    Sends a donation alert to Streamlabs via the API.
    """
    url = "https://streamlabs.com/api/v1.0/donations"

    payload = {
        "access_token": STREAMLABS_TOKEN,  # Token goes in payload for Streamlabs
        "name": battletag,
        "message": message,
        "identifier": str(int(time.time())),
        "amount": amount,
        "currency": "USD"
    }

    try:
        response = requests.post(url, json=payload)
        print(f"Status Code: {response.status_code}")
        print("Response:", response.text)
        return response.status_code == 200
    except Exception as e:
        print("Error sending donation alert:", str(e))
        return False



def get_donations():
    import requests

    import requests

    url = "https://streamlabs.com/api/v2.0/alerts"

    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbiI6IjJGRUE4QjI2MjgxQkMzN0YxMzFDQjJDQjg1RUJDREU2NzIxNDdEQ0M1NjM2MDVCMUE2MEMxNjRCM0Y2QkFFRDk1MkI0NDMyNUVGRDkwNjYxMkIxN0I3RENBRDBFNjkxRTgxQTkyNTg4RTBFNzEzMEVCNTY4NEUwOEU3MzhDQzQ4OTc2NkM1M0I0REEzOTZGMzhDNkQ1RjYwMkYzNjE3MUQ1MkRDNkZCN0RCMEZCOEMyREIwQkNEOURFNzI0QzBFMzNBNUYyNzMxRTRCNTM5MTQzQzgyNDUxQzgwRDU1OERBMkUyMzZDOTYwMzFDNDA2REU3NzU1M0YxNkIiLCJyZWFkX29ubHkiOnRydWUsInByZXZlbnRfbWFzdGVyIjp0cnVlLCJmYWNlYm9va19pZCI6IjUyODU3MjU1ODQ3ODY0MDEiLCJzdHJlYW1sYWJzX2lkIjoiNzI3MDQ5MDk2NTI1NTY1MTMyOCJ9.prfUJ7sJOt79GCjWrYcUU53fO3sXG3gh3nHPRuGO_8w"
    }

    response = requests.post(url, headers=headers)

    print(response.text)
# Test the function
if __name__ == "__main__":
    get_donations()
    # send_streamlabs_alert(5.00, "TestDonor", "Test donation!")