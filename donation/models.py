from django.db import models
from users.models import User
from django.db import models
from django.core.cache import cache
import requests
from decimal import Decimal
import logging

logger = logging.getLogger(__name__)
class Campaign(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='campaigns')
    wallet_address = models.CharField(max_length=100, blank=True, null=True)
    title = models.CharField(max_length=255)
    goal = models.DecimalField(max_digits=10, decimal_places=2)
    collected = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    streamlabs_token = models.TextField(blank=False, null=False)

    def __str__(self):
        return self.title



class Donation(models.Model):
    class Meta:
        ordering = ('-created_at',)

    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name='donations')
    name = models.CharField(max_length=255, blank=True, null=True)
    message = models.TextField(blank=True, null=True)
    amount = models.DecimalField(max_digits=100, decimal_places=20)
    tx_hash = models.CharField(max_length=255, blank=False, null=False)
    currency = models.CharField(max_length=100, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Donation of ${self.amount} to {self.campaign.title}"

    @property
    def formatted_amount(self):
        return float(self.amount)

    @property
    def amount_usd(self):
        """
        Calculate the USD value of the donation using real-time exchange rates.
        Uses cache to avoid hitting API limits.
        """
        if self.currency.upper() == 'USD':
            return self.amount

        # Try to get rate from cache first
        cache_key = f'exchange_rate_{self.currency.lower()}_usd'
        rate = cache.get(cache_key)

        if rate is None:
            try:
                # For crypto currencies (e.g., ETH, BTC)
                if self.currency.upper() in ['ETH', 'BTC', 'USDT']:
                    response = requests.get(
                        f'https://api.coingecko.com/api/v3/simple/price',
                        params={
                            'ids': self._get_coingecko_id(),
                            'vs_currencies': 'usd'
                        },
                        timeout=5
                    )
                    if response.status_code == 200:
                        coin_id = self._get_coingecko_id()
                        rate = Decimal(str(response.json()[coin_id]['usd']))
                else:
                    # For fiat currencies
                    response = requests.get(
                        f'https://api.exchangerate-api.com/v4/latest/USD',
                        timeout=5
                    )
                    if response.status_code == 200:
                        rates = response.json()['rates']
                        # Convert from USD rate to target currency rate
                        rate = Decimal(str(1 / rates[self.currency.upper()]))

                # Cache the rate for 1 hour
                cache.set(cache_key, rate, 3600)
            except Exception as e:
                logger.error(f"Error fetching exchange rate for {self.currency}: {str(e)}")
                return None

        try:
            return self.amount * rate
        except TypeError:
            return None

    def _get_coingecko_id(self):
        """Map common crypto symbols to CoinGecko IDs."""
        crypto_map = {
            'BTC': 'bitcoin',
            'ETH': 'ethereum',
            'USDT': 'tether',
            'USDC': 'tether',
        }
        return crypto_map.get(self.currency.upper(), '')

    @property
    def formatted_amount_usd(self):
        """Return formatted USD amount with proper decimal places."""
        amount = self.amount_usd
        if amount is not None:
            return f"${amount:.2f}"
        return "USD value unavailable"