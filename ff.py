import requests

# Streamlabs API details
AUTHORIZATION_CODE = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiI5ZGE3NjI5Ny02OWMyLTQzMzEtOTFkZi0xY2ViNDZiOTVlYTkiLCJqdGkiOiJlMzE0NDAxMDc0ZDE1OWIwNTk4NjNmODg0ZTExYWFiYTBkZDNjZTYyMTlmZTM4NmVhNzIyODc4NjU2NTc0NWQ1ZjJhNDQ5YzE5NTI3NDU5NSIsImlhdCI6MTczMzQ4ODMxMS4wODU1NzYsIm5iZiI6MTczMzQ4ODMxMS4wODU1NzgsImV4cCI6MjM2NDY0MDMxMS4wNjM1NDIsInN1YiI6IjcxODgyOTgyIiwic2NvcGVzIjpbImRvbmF0aW9ucy5jcmVhdGUiLCJkb25hdGlvbnMucmVhZCIsImFsZXJ0cy5jcmVhdGUiLCJsZWdhY3kudG9rZW4iLCJzb2NrZXQudG9rZW4iLCJwb2ludHMucmVhZCIsInBvaW50cy53cml0ZSIsImFsZXJ0cy53cml0ZSIsImNyZWRpdHMud3JpdGUiLCJwcm9maWxlcy53cml0ZSIsImphci53cml0ZSIsIndoZWVsLndyaXRlIiwibWVkaWFzaGFyZS5jb250cm9sIl19.CuUZ4dkv7IeM6jS32ZCrkK6G8sdoSGgtXZo1N2q3itTw6uapYY1KaFzVOydzoPSStFbcKZjgD7RK52ILeFiZd30NOe5poNaLpnGDbQNgjTbvRWB4UeiSMZQGsjUetgTluWzecWzW4wm_k04YtGHTHrj5uJ44UVAE8Aqul3i-_fOLf-ScnElDSJhW3m_B2ZYh1XAneG46P73dQx3qv3PiFdAChlZzHqZLmCRfH7_z3Pc1Vz9GckWmCMLNxrZIhHgIrKVdYRdruKXE9KNqG01QMw_jvnqwvs4oBPXEPg4qmEIfJpws1vq6NaYpPNrsDbTvGKbL2hEbjCtGCPfxfkdjBmIvp09TW2Tv0ZEXvlwAYtnwEZP-sXcFbdWb-ac9TvYYBGtrAWv1oQ7SJJctdpRm-VLQ0UIqqFPrbiOOvrvbqqzuYIfR716IOki7-Jx8G7q85RxWMhC59VbPxoxPBclKJnm6xj1xcUhbKknVPZmb56YXsuk_L-NWKQZeIXogfnd136jWR_bZ80lsPSvS_5-EVE9uty7dFmzjicBgFsShcWdJ8zF8WTusWNgSKNsZ1WjBLawIRbFaR4ikd17cdeQhSe04FstO2zDjKoCYpp9HqB_LDKbHxxkWzkPJ3igHYei9v6pg_14qrGUEhDsSaLQlXMxc-0EALjYMSQAP6WtYdEI"  # Replace with your code


def exchange_code_for_token():
    """
    Exchanges the authorization code for an access token.
    """
    url = "https://streamlabs.com/api/v2.0/token"
    headers = {
        "Content-Type": "application/json",
        "X-Requested-With": "XMLHttpRequest",
    }
    payload = {
        "grant_type": "authorization_code",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "redirect_uri": REDIRECT_URI,
        "code": AUTHORIZATION_CODE,
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx and 5xx)
        token_data = response.json()

        print("Access Token:", token_data.get("access_token"))
        print("Refresh Token:", token_data.get("refresh_token"))
        print("Expires In:", token_data.get("expires_in"), "seconds")

        # Return the token data for further use
        return token_data

    except requests.exceptions.RequestException as e:
        print("Error exchanging code for token:", e)
        if hasattr(e, 'response') and e.response:
            print("Response:", e.response.text)
        return None


if __name__ == '__main__':
    # Call the function to exchange the authorization code for a token
    token_data = exchange_code_for_token()

    if token_data:
        print("\nToken exchange successful!")
    else:
        print("\nFailed to retrieve token data.")
