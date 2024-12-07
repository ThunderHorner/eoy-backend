from rest_framework.test import APITestCase
from rest_framework import status
from users.models import User
from django.urls import reverse
from donation.models import Campaign, Donation
from api.v1.users.serializers import RegisterUserSerializer


class DonationAPITestCase(APITestCase):
    def setUp(self):
        # Create a user and authenticate
        self.user = User.objects.create_user(email='testemail@test.com', password='password123')
        self.client.login(email='testemail@test.com', password='password123')

        # Obtain JWT token
        token_url = reverse('token_obtain_pair')
        response = self.client.post(token_url, {'email': 'testemail@test.com', 'password': 'password123'})
        self.token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

        # Create a campaign
        self.campaign = Campaign.objects.create(
            user=self.user,
            title="Test Campaign",
            goal=100.0,
            collected=0.0,
            streamlabs_token="eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiI5ZGE3NjI5Ny02OWMyLTQzMzEtOTFkZi0xY2ViNDZiOTVlYTkiLCJqdGkiOiJlMzE0NDAxMDc0ZDE1OWIwNTk4NjNmODg0ZTExYWFiYTBkZDNjZTYyMTlmZTM4NmVhNzIyODc4NjU2NTc0NWQ1ZjJhNDQ5YzE5NTI3NDU5NSIsImlhdCI6MTczMzQ4ODMxMS4wODU1NzYsIm5iZiI6MTczMzQ4ODMxMS4wODU1NzgsImV4cCI6MjM2NDY0MDMxMS4wNjM1NDIsInN1YiI6IjcxODgyOTgyIiwic2NvcGVzIjpbImRvbmF0aW9ucy5jcmVhdGUiLCJkb25hdGlvbnMucmVhZCIsImFsZXJ0cy5jcmVhdGUiLCJsZWdhY3kudG9rZW4iLCJzb2NrZXQudG9rZW4iLCJwb2ludHMucmVhZCIsInBvaW50cy53cml0ZSIsImFsZXJ0cy53cml0ZSIsImNyZWRpdHMud3JpdGUiLCJwcm9maWxlcy53cml0ZSIsImphci53cml0ZSIsIndoZWVsLndyaXRlIiwibWVkaWFzaGFyZS5jb250cm9sIl19.CuUZ4dkv7IeM6jS32ZCrkK6G8sdoSGgtXZo1N2q3itTw6uapYY1KaFzVOydzoPSStFbcKZjgD7RK52ILeFiZd30NOe5poNaLpnGDbQNgjTbvRWB4UeiSMZQGsjUetgTluWzecWzW4wm_k04YtGHTHrj5uJ44UVAE8Aqul3i-_fOLf-ScnElDSJhW3m_B2ZYh1XAneG46P73dQx3qv3PiFdAChlZzHqZLmCRfH7_z3Pc1Vz9GckWmCMLNxrZIhHgIrKVdYRdruKXE9KNqG01QMw_jvnqwvs4oBPXEPg4qmEIfJpws1vq6NaYpPNrsDbTvGKbL2hEbjCtGCPfxfkdjBmIvp09TW2Tv0ZEXvlwAYtnwEZP-sXcFbdWb-ac9TvYYBGtrAWv1oQ7SJJctdpRm-VLQ0UIqqFPrbiOOvrvbqqzuYIfR716IOki7-Jx8G7q85RxWMhC59VbPxoxPBclKJnm6xj1xcUhbKknVPZmb56YXsuk_L-NWKQZeIXogfnd136jWR_bZ80lsPSvS_5-EVE9uty7dFmzjicBgFsShcWdJ8zF8WTusWNgSKNsZ1WjBLawIRbFaR4ikd17cdeQhSe04FstO2zDjKoCYpp9HqB_LDKbHxxkWzkPJ3igHYei9v6pg_14qrGUEhDsSaLQlXMxc-0EALjYMSQAP6WtYdEI"
        )

    def test_create_campaign(self):
        # Test creating a campaign
        url = reverse('campaign-list')
        data = {
            "title": "New Campaign",
            "goal": 200.0,
            "wallet_address": "0xB23a9e81c098aeDeAa829708560c787C9F4c4F47",
            "streamlabs_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiI5ZGE3NjI5Ny02OWMyLTQzMzEtOTFkZi0xY2ViNDZiOTVlYTkiLCJqdGkiOiJlMzE0NDAxMDc0ZDE1OWIwNTk4NjNmODg0ZTExYWFiYTBkZDNjZTYyMTlmZTM4NmVhNzIyODc4NjU2NTc0NWQ1ZjJhNDQ5YzE5NTI3NDU5NSIsImlhdCI6MTczMzQ4ODMxMS4wODU1NzYsIm5iZiI6MTczMzQ4ODMxMS4wODU1NzgsImV4cCI6MjM2NDY0MDMxMS4wNjM1NDIsInN1YiI6IjcxODgyOTgyIiwic2NvcGVzIjpbImRvbmF0aW9ucy5jcmVhdGUiLCJkb25hdGlvbnMucmVhZCIsImFsZXJ0cy5jcmVhdGUiLCJsZWdhY3kudG9rZW4iLCJzb2NrZXQudG9rZW4iLCJwb2ludHMucmVhZCIsInBvaW50cy53cml0ZSIsImFsZXJ0cy53cml0ZSIsImNyZWRpdHMud3JpdGUiLCJwcm9maWxlcy53cml0ZSIsImphci53cml0ZSIsIndoZWVsLndyaXRlIiwibWVkaWFzaGFyZS5jb250cm9sIl19.CuUZ4dkv7IeM6jS32ZCrkK6G8sdoSGgtXZo1N2q3itTw6uapYY1KaFzVOydzoPSStFbcKZjgD7RK52ILeFiZd30NOe5poNaLpnGDbQNgjTbvRWB4UeiSMZQGsjUetgTluWzecWzW4wm_k04YtGHTHrj5uJ44UVAE8Aqul3i-_fOLf-ScnElDSJhW3m_B2ZYh1XAneG46P73dQx3qv3PiFdAChlZzHqZLmCRfH7_z3Pc1Vz9GckWmCMLNxrZIhHgIrKVdYRdruKXE9KNqG01QMw_jvnqwvs4oBPXEPg4qmEIfJpws1vq6NaYpPNrsDbTvGKbL2hEbjCtGCPfxfkdjBmIvp09TW2Tv0ZEXvlwAYtnwEZP-sXcFbdWb-ac9TvYYBGtrAWv1oQ7SJJctdpRm-VLQ0UIqqFPrbiOOvrvbqqzuYIfR716IOki7-Jx8G7q85RxWMhC59VbPxoxPBclKJnm6xj1xcUhbKknVPZmb56YXsuk_L-NWKQZeIXogfnd136jWR_bZ80lsPSvS_5-EVE9uty7dFmzjicBgFsShcWdJ8zF8WTusWNgSKNsZ1WjBLawIRbFaR4ikd17cdeQhSe04FstO2zDjKoCYpp9HqB_LDKbHxxkWzkPJ3igHYei9v6pg_14qrGUEhDsSaLQlXMxc-0EALjYMSQAP6WtYdEI"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.json())
        self.assertEqual(response.data['title'], "New Campaign")

    def test_get_campaign_list(self):
        # Test fetching a list of campaigns
        url = reverse('campaign-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Only one campaign in the setup

    def test_get_campaign_detail(self):
        # Test fetching a single campaign's details
        url = reverse('campaign-detail', kwargs={'pk': self.campaign.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], "Test Campaign")

    def test_update_campaign(self):
        # Test updating a campaign's goal
        url = reverse('campaign-detail', kwargs={'pk': self.campaign.id})
        data = {"goal": 150.0}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['goal'], "150.00")  # Updated goal

    def test_delete_campaign(self):
        # Test deleting a campaign
        url = reverse('campaign-detail', kwargs={'pk': self.campaign.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_create_donation(self):
        # Test creating a donation for a campaign
        url = reverse('donate', kwargs={'campaign_id': self.campaign.id})
        data = {
            "name": "Kostas",
            "message": "Test donation",
            "amount": "0.05",
            'currency':'BTC',
            "campaign": self.campaign.id,
            "tx_hash": "0xeb818a145cdc40d77c4d7f7078479742d48df1cde216bbbbb97374bae5d35a45"
        }


        """
        {name: "Kosta", message: "Test", amount: "0.05", campaign: "9", currency: "ETH",…}
amount
: 
"0.05"
campaign
: 
"9"
currency
: 
"ETH"
message
: 
"Test"name:"Kosta"
request_id: "0122a7903a7c081307ed39ab30d9123f9f87bcc99ce0047844f681c1b1585a4015"
        """
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.json())
        self.assertEqual(response.data['name'], data['name'])
        self.assertEqual(response.data['message'], data['message'])
        self.assertEqual(response.data['tx_hash'], data['tx_hash'])
        self.assertEqual(response.data['currency'], data['currency'])
        self.assertEqual(float(response.data['amount']), float(data['amount']))

    def test_create_donation_invalid_campaign(self):
        # Test donating to a non-existent campaign
        url = reverse('donate', kwargs={'campaign_id': 9999})
        data = {
            "name": "John Doe",
            "message": "Keep it up!",
            "amount": 20.0
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['error'], "Campaign not found")

    def test_register_user(self):
        data = {
            'email': 'testemail2@test.com',
            'battletag': 'Battle#1234',
            'password': 'test_password'
        }

        serializer = RegisterUserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
        url = reverse('register')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201, response.json())

        user = User.objects.get(email='testemail2@test.com')
        # Assert user is created
        assert user is not None

        # Assert the user instance is the same one returned from our RegisterUserSerializer

        assert serializer.instance == user

        # Assert the details are correct
        assert user.email == data['email']
        assert user.battletag == data['battletag']
        assert user.check_password(data['password'])
