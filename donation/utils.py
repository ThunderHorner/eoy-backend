import requests


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
