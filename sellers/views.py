from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.db.models import Sum

from .models import SellerProfile
from .serializers import SellerProfileSerializer
from products.models import Product
from products.serializers import ProductListSerializer
from orders.models import OrderItem, Order
from orders.serializers import OrderSerializer


class SellerProfileView(generics.RetrieveUpdateAPIView):
    serializer_class   = SellerProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        profile, _ = SellerProfile.objects.get_or_create(
            user=self.request.user,
            defaults={'store_slug': f'store-{self.request.user.id}'}
        )
        return profile


class SellerPublicView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, user_id):
        from users.models import User
        seller   = get_object_or_404(User, id=user_id)
        profile  = getattr(seller, 'seller_profile', None)
        products = Product.objects.filter(seller=seller, is_active=True)
        return Response({
            'id':          seller.id,
            'name':        seller.full_name,
            'store_name':  profile.store_name if profile else seller.full_name,
            'store_desc':  profile.store_desc if profile else '',
            'product_count': products.count(),
            'products':    ProductListSerializer(products, many=True, context={'request': request}).data,
        })


class SellerDashboardView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        from django.utils import timezone
        from datetime import timedelta

        user          = request.user
        products      = Product.objects.filter(seller=user)
        order_items   = OrderItem.objects.filter(seller=user)
        total_revenue = order_items.aggregate(total=Sum('product_price'))['total'] or 0
        total_sales   = order_items.count()

        cutoff = timezone.now() - timedelta(days=7)
        pending_revenue = order_items.filter(
            order__created_at__gte=cutoff
        ).aggregate(total=Sum('product_price'))['total'] or 0
        withdrawable_revenue = order_items.filter(
            order__created_at__lt=cutoff
        ).aggregate(total=Sum('product_price'))['total'] or 0

        total_views = products.aggregate(total=Sum('view_count'))['total'] or 0
        conversion_rate = round((total_sales / total_views) * 100, 1) if total_views > 0 else 0

        top_products = products.order_by('-sales_count')[:5]
        top_products_data = [
            {
                'id': p.id,
                'name': p.name,
                'sales_count': p.sales_count,
                'view_count': p.view_count,
                'revenue': float(p.price) * p.sales_count,
            }
            for p in top_products
        ]

        recent_orders = Order.objects.filter(
            items__seller=user
        ).distinct().order_by('-created_at')[:5]
        return Response({
            'total_revenue':        float(total_revenue),
            'pending_revenue':      float(pending_revenue),
            'withdrawable_revenue': float(withdrawable_revenue),
            'total_sales':          total_sales,
            'product_count':        products.count(),
            'total_views':          total_views,
            'conversion_rate':      conversion_rate,
            'top_products':         top_products_data,
            'recent_orders':        OrderSerializer(recent_orders, many=True).data,
        })