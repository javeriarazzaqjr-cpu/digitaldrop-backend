from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Order
from .serializers import OrderSerializer, CheckoutSerializer, CouponValidateSerializer
from cart.models import CartItem


class OrderListView(generics.ListAPIView):
    serializer_class   = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(buyer=self.request.user).prefetch_related('items__product')


class OrderDetailView(generics.RetrieveAPIView):
    serializer_class   = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(buyer=self.request.user).prefetch_related('items__product')


class CheckoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        import stripe
        from django.conf import settings
        stripe.api_key = settings.STRIPE_SECRET_KEY

        cart_items = CartItem.objects.filter(user=request.user).select_related('product')
        if not cart_items.exists():
            return Response({'detail': 'Cart is empty.'}, status=status.HTTP_400_BAD_REQUEST)

        s = CheckoutSerializer(data=request.data)
        s.is_valid(raise_exception=True)

        # Verify payment with Stripe
        payment_intent_id = s.validated_data['payment_intent_id']
        try:
            intent = stripe.PaymentIntent.retrieve(payment_intent_id)
        except stripe.error.StripeError as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        if intent.status != 'succeeded':
            return Response({'detail': 'Payment not completed.'}, status=status.HTTP_400_BAD_REQUEST)

        order = s.create_order(request.user, cart_items)
        cart_items.delete()

        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)


class CouponValidateView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        s = CouponValidateSerializer(data=request.data)
        s.is_valid(raise_exception=True)
        coupon = s.validated_data['code']
        return Response({'discount_pct': coupon.discount_pct, 'code': coupon.code})


class SellerOrdersView(generics.ListAPIView):
    serializer_class   = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        order_ids = Order.objects.filter(
            items__seller=self.request.user
        ).values_list('id', flat=True).distinct()
        return Order.objects.filter(id__in=order_ids).prefetch_related('items__product')