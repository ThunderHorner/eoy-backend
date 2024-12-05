from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from donation.models import Campaign, Donation

class DonationAPITestCase(APITestCase):
    def setUp(self):
        # Create a user and authenticate
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.client.login(username='testuser', password='password123')

        # Obtain JWT token
        response = self.client.post('/token/', {'username': 'testuser', 'password': 'password123'})
        self.token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

        # Create a campaign
        self.campaign = Campaign.objects.create(
            user=self.user,
            title="Test Campaign",
            goal=100.0,
            collected=0.0
        )

    def test_create_campaign(self):
        # Test creating a campaign
        data = {
            "title": "New Campaign",
            "goal": 200.0
        }
        response = self.client.post('/donation/campaigns/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], "New Campaign")

    def test_get_campaign_list(self):
        # Test fetching a list of campaigns
        response = self.client.get('/donation/campaigns/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Only one campaign in the setup

    def test_get_campaign_detail(self):
        # Test fetching a single campaign's details
        response = self.client.get(f'/donation/campaigns/{self.campaign.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], "Test Campaign")

    def test_update_campaign(self):
        # Test updating a campaign's goal
        data = {"goal": 150.0}
        response = self.client.patch(f'/donation/campaigns/{self.campaign.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['goal'], "150.00")  # Updated goal

    def test_delete_campaign(self):
        # Test deleting a campaign
        response = self.client.delete(f'/donation/campaigns/{self.campaign.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_create_donation(self):
        # Test creating a donation for a campaign
        data = {
            "name": "Anonymous",
            "message": "Great work!",
            "amount": 50.0
        }
        response = self.client.post(f'/donation/campaigns/{self.campaign.id}/donate/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], "Anonymous")
        self.assertEqual(response.data['amount'], "50.00")

    def test_create_donation_invalid_campaign(self):
        # Test donating to a non-existent campaign
        data = {
            "name": "John Doe",
            "message": "Keep it up!",
            "amount": 20.0
        }
        response = self.client.post('/donation/campaigns/9999/donate/', data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['error'], "Campaign not found")
