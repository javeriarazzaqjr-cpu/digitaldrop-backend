from django.db import models
from django.conf import settings


class SellerProfile(models.Model):
    user           = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                          related_name='seller_profile')
    store_name     = models.CharField(max_length=200, blank=True)
    store_slug     = models.SlugField(unique=True, max_length=200, blank=True)
    store_desc     = models.TextField(blank=True)
    payout_method  = models.CharField(max_length=50, default='paypal')
    payout_account = models.CharField(max_length=200, blank=True)
    min_payout     = models.DecimalField(max_digits=8, decimal_places=2, default=50)
    notify_sale    = models.BooleanField(default=True)
    notify_review  = models.BooleanField(default=True)
    created_at     = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.store_name or self.user.full_name