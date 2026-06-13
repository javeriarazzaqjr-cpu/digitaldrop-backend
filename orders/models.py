from django.db import models
from django.conf import settings
import uuid


class Coupon(models.Model):
    code         = models.CharField(max_length=30, unique=True)
    discount_pct = models.PositiveSmallIntegerField()
    is_active    = models.BooleanField(default=True)
    expires_at   = models.DateTimeField(null=True, blank=True)
    used_count   = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'{self.code} ({self.discount_pct}%)'


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending',   'Pending'),
        ('completed', 'Completed'),
        ('refunded',  'Refunded'),
        ('failed',    'Failed'),
    ]

    order_number = models.CharField(max_length=20, unique=True, editable=False)
    buyer        = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
                                     null=True, related_name='purchases')
    buyer_email  = models.EmailField()
    buyer_name   = models.CharField(max_length=160)
    subtotal     = models.DecimalField(max_digits=10, decimal_places=2)
    discount     = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total        = models.DecimalField(max_digits=10, decimal_places=2)
    coupon       = models.ForeignKey(Coupon, on_delete=models.SET_NULL, null=True, blank=True)
    status       = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at   = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.order_number:
            self.order_number = 'ORD-' + uuid.uuid4().hex[:8].upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.order_number


class OrderItem(models.Model):
    order         = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product       = models.ForeignKey('products.Product', on_delete=models.SET_NULL, null=True)
    product_name  = models.CharField(max_length=200)
    product_price = models.DecimalField(max_digits=10, decimal_places=2)
    seller        = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
                                      null=True, related_name='sales')