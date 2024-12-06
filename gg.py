import requests
from urllib.parse import quote

# Constants
CLIENT_ID = "9da76297-69c2-4331-91df-1ceb46b95ea9"
CLIENT_SECRET = "dk45lJxt8vXzgdgFstdbuYmo0Upv4tR8Ywr5ZqRR"
REDIRECT_URI = "https://3a795c30ad8b.ngrok.app/auth"
BASE_URL = "https://streamlabs.com/api/v2.0"


def get_auth_url():
    """Generate the authorization URL with properly encoded scopes."""
    scopes = [
        'donations.create',
        'donations.read',
        'alerts.create',
        'legacy.token',
        'socket.token',
        'points.read',
        'points.write',
        'alerts.write',
        'credits.write',
        'profiles.write',
        'jar.write',
        'wheel.write',
        'mediashare.control'
    ]
    # Properly URL encode the scopes
    encoded_scopes = quote(' '.join(scopes))

    auth_url = (
        f"{BASE_URL}/authorize"
        f"?client_id={CLIENT_ID}"
        f"&redirect_uri={REDIRECT_URI}"
        f"&response_type=code"
        f"&scope={encoded_scopes}"
    )
    return auth_url


def get_access_token(auth_code):
    """Exchange authorization code for access token."""
    token_url = f"{BASE_URL}/token"
    data = {
        "grant_type": "authorization_code",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "redirect_uri": REDIRECT_URI,
        "code": auth_code.strip(),
    }

    try:
        response = requests.post(token_url, data=data)
        response.raise_for_status()  # Raise an exception for bad status codes
        return response.json()["access_token"]
    except requests.exceptions.RequestException as e:
        raise Exception(
            f"Error getting token: {str(e)}\nResponse: {response.text if 'response' in locals() else 'No response'}")


def fetch_donations(access_token, limit=10):
    """Fetch recent donations."""
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/json"
    }

    donations_url = f"{BASE_URL}/donations"
    params = {"limit": limit}

    try:
        response = requests.get(donations_url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise Exception(
            f"Error fetching donations: {str(e)}\nResponse: {response.text if 'response' in locals() else 'No response'}")


def add_donation(access_token, name, identifier, amount, currency, message):
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


def main():
    """Main execution flow with error handling."""
    try:
        print("Step 1: Authorize the App")
        print("Visit this URL to authorize the app:")
        print(get_auth_url())

        auth_code = input("\nEnter the authorization code you received: ").strip()
        access_token = get_access_token(auth_code)
        print(f"Access Token: {access_token}")

        print("\nFetching recent donations...")
        donations = fetch_donations(access_token)
        print("Recent donations:", donations)

        # Optional: Add test donation
        proceed = input("\nWould you like to add a test donation? (y/n): ").lower()
        if proceed == 'y':
            new_donation = add_donation(
                access_token=access_token,
                name="Test Donor",
                identifier="test@example.com",
                amount=5.00,
                currency="ETH",
                message="This is a test donation!"
            )
            print("Test donation response:", new_donation)

    except Exception as e:
        print(f"An error occurred: {str(e)}")


if __name__ == "__main__":
    main()