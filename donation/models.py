from django.db import models
from users.models import User

class Campaign(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='campaigns')
    wallet_address = models.CharField(max_length=100, blank=True, null=True)
    title = models.CharField(max_length=255)
    goal = models.DecimalField(max_digits=10, decimal_places=2)
    collected = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Donation(models.Model):
    class Meta:
        ordering = ('-created_at',)
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name='donations')
    name = models.CharField(max_length=255, blank=True, null=True)
    message = models.TextField(blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Donation of ${self.amount} to {self.campaign.title}"
