from rest_framework import serializers
from .models import Order, OrderItem, Coupon
from django.utils import timezone


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model  = OrderItem
        fields = ('id', 'product', 'product_name', 'product_price')


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model  = Order
        fields = ('id', 'order_number', 'buyer_email', 'buyer_name',
                  'subtotal', 'discount', 'total', 'status', 'created_at', 'items')
        read_only_fields = ('id', 'order_number', 'status', 'created_at')


class CheckoutSerializer(serializers.Serializer):
    email      = serializers.EmailField()
    first_name = serializers.CharField(max_length=80)
    last_name  = serializers.CharField(max_length=80, required=False, default='')
    coupon     = serializers.CharField(required=False, allow_blank=True)
    payment_intent_id = serializers.CharField(max_length=200)

    def validate_coupon(self, value):
        if not value:
            return None
        try:
            coupon = Coupon.objects.get(code=value.upper(), is_active=True)
            if coupon.expires_at and coupon.expires_at < timezone.now():
                raise serializers.ValidationError('Coupon has expired.')
            return coupon
        except Coupon.DoesNotExist:
            raise serializers.ValidationError('Invalid coupon code.')

    def create_order(self, user, cart_items):
        coupon   = self.validated_data.get('coupon')
        subtotal = sum(item.product.price for item in cart_items)
        discount = 0
        if coupon:
            discount = round(subtotal * coupon.discount_pct / 100, 2)
            coupon.used_count += 1
            coupon.save()
        total = subtotal - discount

        order = Order.objects.create(
            buyer       = user if user.is_authenticated else None,
            buyer_email = self.validated_data['email'],
            buyer_name  = f"{self.validated_data['first_name']} {self.validated_data.get('last_name','')}".strip(),
            subtotal    = subtotal,
            discount    = discount,
            total       = total,
            coupon      = coupon,
            status      = 'completed',
        )
        for item in cart_items:
            p = item.product
            OrderItem.objects.create(
                order=order, product=p,
                product_name=p.name, product_price=p.price,
                seller=p.seller,
            )
            p.sales_count += 1
            p.save(update_fields=['sales_count'])

        return order


class CouponValidateSerializer(serializers.Serializer):
    code = serializers.CharField()

    def validate_code(self, value):
        try:
            coupon = Coupon.objects.get(code=value.upper(), is_active=True)
            return coupon
        except Coupon.DoesNotExist:
            raise serializers.ValidationError('Invalid or expired coupon.')