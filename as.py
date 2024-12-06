import requests


def get_streamlabs_donations(access_token):
    """
    Fetch donations from Streamlabs API

    Args:
        access_token (str): Your Streamlabs OAuth access token

    Returns:
        dict: JSON response from the API
    """
    url = "https://streamlabs.com/api/v2.0/donations"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "accept": "application/json"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for bad status codes
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error making request: {e}")
        return None


# Example usage
if __name__ == "__main__":
    access_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbiI6IjQxNUQ5MDlFREFFREY1QkQ0QTYzRkZDQTM1NjY4RDI5MDI5NEFGNDUwQ0IzOUQ2NzkwODE4RTgzMDZBOEU5OUYyMTJFQUJDNDBDQUZFRjJGRTgwQTc4MzgyREQ1RDhCMjE5QTUzRjk4NkNGMjlBMjZGNDNDNUJDNTczMjFEN0Q1Q0Y4RENCN0RDNzI2NTlGMjAwN0YxRTdBQzE1Qzc0MDhEODcyMDAwODcyNjBGOUQyNUFCRjkyQTk2MURDRDFBNjhBQzAyQzI5NUY2MDFBMTI2NEZDMDI5OUM0N0Q3NUIwMEU1MzA1NEU5N0E4RDQxRUVGRTZGNDYxMTciLCJyZWFkX29ubHkiOnRydWUsInByZXZlbnRfbWFzdGVyIjp0cnVlLCJmYWNlYm9va19pZCI6IjUyODU3MjU1ODQ3ODY0MDEiLCJzdHJlYW1sYWJzX2lkIjoiNzI3MDQ5MDk2NTI1NTY1MTMyOCIsInlvdXR1YmVfaWQiOiJVQ09OUkt4VFFtVHNPUm9UZGV0dVFWM2cifQ.x8niJlJu-gqBLhQ5nRDmAIf9qEC5qFQkATlTvQvWhyY"  # Replace with your actual access token
    donations = get_streamlabs_donations(access_token)

    if donations:
        print(donations)