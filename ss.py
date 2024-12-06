import requests
from urllib.parse import urljoin


def fetch_donations(access_token):
    """
    Fetch donations from Streamlabs API

    Args:
        access_token (str): Your Streamlabs API access token

    Returns:
        dict: JSON response containing donation data
    """
    base_url = "https://streamlabs.com/api/v2.0/"
    donations_endpoint ="https://streamlabs.com/api/v2.0/donations"
    print(donations_endpoint)
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": 'Bearer %s'%access_token
    }

    try:
        response = requests.get(
            donations_endpoint,
            headers=headers,
            timeout=10
        )
        print(response.status_code)
        response.raise_for_status()  # Raises an HTTPError for bad responses

        return response.json()

    except requests.exceptions.HTTPError as http_err:
        if response.status_code == 401:
            raise Exception("Invalid or expired access token. Please check your credentials.")
        elif response.status_code == 404:
            raise Exception("API endpoint not found. Please verify the API version.")
        else:
            raise Exception(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as err:
        raise Exception(f"Error occurred while fetching donations: {err}")


if __name__ == '__main__':
    # Replace with your actual access token
    ACCESS_TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbiI6IjQxNUQ5MDlFREFFREY1QkQ0QTYzRkZDQTM1NjY4RDI5MDI5NEFGNDUwQ0IzOUQ2NzkwODE4RTgzMDZBOEU5OUYyMTJFQUJDNDBDQUZFRjJGRTgwQTc4MzgyREQ1RDhCMjE5QTUzRjk4NkNGMjlBMjZGNDNDNUJDNTczMjFEN0Q1Q0Y4RENCN0RDNzI2NTlGMjAwN0YxRTdBQzE1Qzc0MDhEODcyMDAwODcyNjBGOUQyNUFCRjkyQTk2MURDRDFBNjhBQzAyQzI5NUY2MDFBMTI2NEZDMDI5OUM0N0Q3NUIwMEU1MzA1NEU5N0E4RDQxRUVGRTZGNDYxMTciLCJyZWFkX29ubHkiOnRydWUsInByZXZlbnRfbWFzdGVyIjp0cnVlLCJmYWNlYm9va19pZCI6IjUyODU3MjU1ODQ3ODY0MDEiLCJzdHJlYW1sYWJzX2lkIjoiNzI3MDQ5MDk2NTI1NTY1MTMyOCJ9.GRyKHZbmjkojpppWlkxJJQrZI-WfYKnIFCZDcA6GuYs"

    try:
        donations = fetch_donations(ACCESS_TOKEN)
        print("Donations retrieved successfully:")
        print(donations)
    except Exception as e:
        print(f"Error: {e}")


"""

donations.create	POST /donations
donations.read	GET /donations
alerts.create	POST /alerts
legacy.token	GET /legacy/token
socket.token	GET /socket/token
points.read	GET /points
points.write	POST /points/subtract
alerts.write	POST /alerts/skip
credits.write	POST /credits/roll
profiles.write	GET /alert_profiles/get
jar.write	POST /jar/empty
wheel.write	POST /wheel/spin
mediashare.control	PUT media-share/play-media

"""