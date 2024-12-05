from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics, permissions
from donation.models import Campaign, Donation
from .serializers import CampaignSerializer, DonationSerializer
from django.db.models import F


class CampaignListCreateView(generics.ListCreateAPIView):
    queryset = Campaign.objects.all()
    serializer_class = CampaignSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)



class CampaignDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Campaign.objects.all()
    serializer_class = CampaignSerializer

    def get_permissions(self):
        """
        Allow any user to retrieve a campaign, but restrict updates and deletions to authenticated users.
        """
        if self.request.method in permissions.SAFE_METHODS:  # SAFE_METHODS = ['GET', 'HEAD', 'OPTIONS']
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]  # For PUT, PATCH, DELETE

    def perform_update(self, serializer):
        serializer.save()


class DonationCreateView(APIView):
    permission_classes = [
        permissions.AllowAny,
    ]
    def post(self, request, campaign_id):
        try:
            campaign = Campaign.objects.get(pk=campaign_id)
        except Campaign.DoesNotExist:
            return Response({"error": "Campaign not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = DonationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(campaign=campaign)
            campaign.collected = F('collected') + serializer.validated_data['amount']
            campaign.save(update_fields=['collected'])
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, campaign_id):
        try:
            # Fetch the campaign
            campaign = Campaign.objects.get(pk=campaign_id)
        except Campaign.DoesNotExist:
            return Response({"error": "Campaign not found"}, status=status.HTTP_404_NOT_FOUND)

        # Serialize the donations for the campaign
        donations = Donation.objects.filter(campaign=campaign)
        serializer = DonationSerializer(donations, many=True)

        # Return serialized data
        return Response(serializer.data, status=status.HTTP_200_OK)