import stripe
from django.conf import settings
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from cart.models import CartItem

stripe.api_key = settings.STRIPE_SECRET_KEY


class CreatePaymentIntentView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        cart_items = CartItem.objects.filter(user=request.user).select_related('product')
        if not cart_items.exists():
            return Response({'detail': 'Cart is empty.'}, status=status.HTTP_400_BAD_REQUEST)

        subtotal = sum(item.product.price for item in cart_items)

        coupon_code = request.data.get('coupon', '')
        discount = 0
        if coupon_code:
            from orders.models import Coupon
            try:
                coupon = Coupon.objects.get(code=coupon_code.upper(), is_active=True)
                discount = round(subtotal * coupon.discount_pct / 100, 2)
            except Coupon.DoesNotExist:
                pass

        total = subtotal - discount
        amount_in_cents = int(total * 100)

        try:
            intent = stripe.PaymentIntent.create(
                amount=amount_in_cents,
                currency='usd',
                metadata={'user_id': str(request.user.id)},
                automatic_payment_methods={'enabled': True},
            )
            return Response({
                'client_secret': intent.client_secret,
                'amount': total,
            })
        except stripe.error.StripeError as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)