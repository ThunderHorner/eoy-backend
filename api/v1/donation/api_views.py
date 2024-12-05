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
    permission_classes = [permissions.IsAuthenticated]

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
