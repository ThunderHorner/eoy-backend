from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics, permissions
from donation.models import Campaign, Donation
from donation.utils import add_donation
from .serializers import CampaignSerializer, DonationSerializer
from django.db.models import F
from django.db import transaction
from django.db.models import F
from rest_framework import status
from rest_framework.response import Response

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
            with transaction.atomic():
                try:
                    campaign = Campaign.objects.get(pk=campaign_id)
                except Campaign.DoesNotExist:
                    return Response({"error": "Campaign not found"}, status=status.HTTP_404_NOT_FOUND)

                serializer = DonationSerializer(data=request.data)
                if serializer.is_valid(raise_exception=True):
                    donation = serializer.save(campaign=campaign)

                    campaign.collected = F('collected') + donation.amount_usd
                    campaign.save(update_fields=['collected'])

                    try:
                        add_donation(
                            access_token=campaign.user.streamlabs_token,
                            name=donation.name,
                            identifier=donation.tx_hash,
                            amount=float(donation.amount),
                            message=f"{donation.message or ''}" ,
                            currency="USD"
                        )
                    except Exception as e:
                        print(f"Streamlabs notification failed: {str(e)}")
                    return Response(serializer.data, status=status.HTTP_201_CREATED)

                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            # logger.error(f"Donation processing failed: {str(e)}")
            return Response(
                {"error": "Failed to process donation"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

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