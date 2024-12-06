import requests

BASE_URL = "https://streamlabs.com/api/v2.0"

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



if __name__ == "__main__":
    access_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiI5ZGE3NjI5Ny02OWMyLTQzMzEtOTFkZi0xY2ViNDZiOTVlYTkiLCJqdGkiOiJlMzE0NDAxMDc0ZDE1OWIwNTk4NjNmODg0ZTExYWFiYTBkZDNjZTYyMTlmZTM4NmVhNzIyODc4NjU2NTc0NWQ1ZjJhNDQ5YzE5NTI3NDU5NSIsImlhdCI6MTczMzQ4ODMxMS4wODU1NzYsIm5iZiI6MTczMzQ4ODMxMS4wODU1NzgsImV4cCI6MjM2NDY0MDMxMS4wNjM1NDIsInN1YiI6IjcxODgyOTgyIiwic2NvcGVzIjpbImRvbmF0aW9ucy5jcmVhdGUiLCJkb25hdGlvbnMucmVhZCIsImFsZXJ0cy5jcmVhdGUiLCJsZWdhY3kudG9rZW4iLCJzb2NrZXQudG9rZW4iLCJwb2ludHMucmVhZCIsInBvaW50cy53cml0ZSIsImFsZXJ0cy53cml0ZSIsImNyZWRpdHMud3JpdGUiLCJwcm9maWxlcy53cml0ZSIsImphci53cml0ZSIsIndoZWVsLndyaXRlIiwibWVkaWFzaGFyZS5jb250cm9sIl19.CuUZ4dkv7IeM6jS32ZCrkK6G8sdoSGgtXZo1N2q3itTw6uapYY1KaFzVOydzoPSStFbcKZjgD7RK52ILeFiZd30NOe5poNaLpnGDbQNgjTbvRWB4UeiSMZQGsjUetgTluWzecWzW4wm_k04YtGHTHrj5uJ44UVAE8Aqul3i-_fOLf-ScnElDSJhW3m_B2ZYh1XAneG46P73dQx3qv3PiFdAChlZzHqZLmCRfH7_z3Pc1Vz9GckWmCMLNxrZIhHgIrKVdYRdruKXE9KNqG01QMw_jvnqwvs4oBPXEPg4qmEIfJpws1vq6NaYpPNrsDbTvGKbL2hEbjCtGCPfxfkdjBmIvp09TW2Tv0ZEXvlwAYtnwEZP-sXcFbdWb-ac9TvYYBGtrAWv1oQ7SJJctdpRm-VLQ0UIqqFPrbiOOvrvbqqzuYIfR716IOki7-Jx8G7q85RxWMhC59VbPxoxPBclKJnm6xj1xcUhbKknVPZmb56YXsuk_L-NWKQZeIXogfnd136jWR_bZ80lsPSvS_5-EVE9uty7dFmzjicBgFsShcWdJ8zF8WTusWNgSKNsZ1WjBLawIRbFaR4ikd17cdeQhSe04FstO2zDjKoCYpp9HqB_LDKbHxxkWzkPJ3igHYei9v6pg_14qrGUEhDsSaLQlXMxc-0EALjYMSQAP6WtYdEI'
    new_donation = add_donation(
        access_token=access_token,
        name="Test Donor",
        identifier="test@example.com",
        amount=5.00,
        currency="USD",
        message="This is a test donation!"
    )