from django.urls import path
from api.v1.donation.api_views import DonationCreateView, CampaignListCreateView, CampaignDetailView

urlpatterns = [
    path('campaigns/', CampaignListCreateView.as_view(), name='campaign-list'),
    path('campaigns/<int:pk>/', CampaignDetailView.as_view(), name='campaign-detail'),
    path('campaigns/<int:campaign_id>/donate/', DonationCreateView.as_view(), name='donate'),
]
