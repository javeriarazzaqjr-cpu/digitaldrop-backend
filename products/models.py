from django.db import models
from django.conf import settings


class Category(models.Model):
    name  = models.CharField(max_length=80, unique=True)
    emoji = models.CharField(max_length=10, blank=True)
    slug  = models.SlugField(unique=True)

    class Meta:
        verbose_name_plural = 'categories'
        ordering = ['name']

    def __str__(self):
        return self.name


class Product(models.Model):
    BADGE_CHOICES = [
        ('hot',        'Hot'),
        ('new',        'New'),
        ('bestseller', 'Bestseller'),
    ]

    seller      = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='products')
    name        = models.CharField(max_length=200)
    description = models.TextField()
    category    = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='products')
    price       = models.DecimalField(max_digits=10, decimal_places=2)
    old_price   = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    emoji       = models.CharField(max_length=10, default='📦')
    file        = models.FileField(upload_to='products/', blank=True, null=True)
    badge = models.CharField(max_length=20, choices=BADGE_CHOICES, blank=True, default='')
    tags        = models.CharField(max_length=300, blank=True)
    sales_count = models.PositiveIntegerField(default=0)
    is_active   = models.BooleanField(default=True)
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    @property
    def avg_rating(self):
        reviews = self.reviews.all()
        if not reviews:
            return 0
        return round(sum(r.rating for r in reviews) / len(reviews), 1)

    @property
    def review_count(self):
        return self.reviews.count()

    @property
    def discount_percent(self):
        if self.old_price and self.old_price > self.price:
            return round((1 - self.price / self.old_price) * 100)
        return 0

    def __str__(self):
        return self.name


class ProductInclude(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='includes')
    item    = models.CharField(max_length=200)
    order   = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ['order']


class Review(models.Model):
    product    = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    author     = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating     = models.PositiveSmallIntegerField()
    text       = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('product', 'author')
        ordering = ['-created_at']


class Wishlist(models.Model):
    user     = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='wishlist')
    product  = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='wishlisted_by')
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')