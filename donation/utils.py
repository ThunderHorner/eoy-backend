import requests

CLIENT_ID = "9da76297-69c2-4331-91df-1ceb46b95ea9"
CLIENT_SECRET = "dk45lJxt8vXzgdgFstdbuYmo0Upv4tR8Ywr5ZqRR"
REDIRECT_URI = "https://3a795c30ad8b.ngrok.app/auth"
BASE_URL = "https://streamlabs.com/api/v2.0"


def add_donation(*, access_token, name, identifier, amount, currency, message):
    BASE_URL = "https://streamlabs.com/api/v2.0"

    """Add a new donation."""
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    donation_url = f"{BASE_URL}/donations"
    data = {
        "name": name,
        "identifier": identifier,
        "amount": float(amount),  # Ensure amount is float
        "currency": currency.upper(),  # Ensure currency is uppercase
        "message": message
    }

    try:
        response = requests.post(donation_url, headers=headers, json=data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise Exception(
            f"Error adding donation: {str(e)}\nResponse: {response.text if 'response' in locals() else 'No response'}")



def get_user(*, access_token):
    BASE_URL = "https://streamlabs.com/api/v2.0"

    """Add a new donation."""
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    donation_url = f"{BASE_URL}/user"

    try:
        response = requests.get(donation_url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise Exception(
            f"Error adding donation: {str(e)}\nResponse: {response.text if 'response' in locals() else 'No response'}")


def get_access_token(auth_code):
    BASE_URL = "https://streamlabs.com/api/v2.0"
    """Exchange authorization code for access token."""
    token_url = f"{BASE_URL}/token"
    data = {
        "grant_type": "authorization_code",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "redirect_uri": REDIRECT_URI,
        "code": auth_code.strip(),
    }
    print(data)

    try:
        response = requests.post(token_url, data=data)
        response.raise_for_status()  # Raise an exception for bad status codes
        return response.json()["access_token"]
    except requests.exceptions.RequestException as e:
        return ''
