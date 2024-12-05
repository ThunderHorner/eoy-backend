from rest_framework import serializers
from donation.models import Campaign, Donation

class CampaignSerializer(serializers.ModelSerializer):
    collected = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Campaign
        fields = ['id', 'title', 'goal', 'collected', 'user', 'created_at', 'updated_at']
        read_only_fields = ['user', 'created_at', 'updated_at']

class DonationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Donation
        fields = ['id', 'campaign', 'name', 'message', 'amount', 'created_at']
        read_only_fields = ['created_at']