from django.db import models
from rest_framework import generics, permissions, status, filters
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from .models import Category, Product, Review, Wishlist
from .serializers import (
    CategorySerializer, ProductListSerializer, ProductDetailSerializer,
    ProductCreateSerializer, ReviewSerializer, WishlistSerializer
)

from .filters import ProductFilter
from django.http import FileResponse
from orders.models import OrderItem

class CategoryListView(generics.ListAPIView):
    queryset           = Category.objects.all()
    serializer_class   = CategorySerializer
    permission_classes = [permissions.AllowAny]


class ProductListView(generics.ListAPIView):
    serializer_class   = ProductListSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends    = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class    = ProductFilter
    search_fields      = ['name', 'description', 'tags']
    ordering_fields    = ['price', 'created_at', 'sales_count']
    ordering           = ['-created_at']

    def get_queryset(self):
        return Product.objects.filter(is_active=True).select_related('seller', 'category').prefetch_related('reviews')


class ProductDetailView(generics.RetrieveAPIView):
    serializer_class   = ProductDetailSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return Product.objects.filter(is_active=True).select_related('seller', 'category').prefetch_related('reviews', 'includes')

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        Product.objects.filter(pk=instance.pk).update(view_count=models.F('view_count') + 1)
        instance.refresh_from_db()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

class ProductCreateView(generics.CreateAPIView):
    serializer_class   = ProductCreateSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes     = [MultiPartParser, FormParser, JSONParser]

    def perform_create(self, serializer):
        if self.request.user.role not in ('seller', 'both'):
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied('Only sellers can add products. Update your account role in your profile to start selling.')
        serializer.save(seller=self.request.user)


class ProductUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class   = ProductCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Product.objects.filter(seller=self.request.user)


class MyProductsView(generics.ListAPIView):
    serializer_class   = ProductListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Product.objects.filter(seller=self.request.user).select_related('category').prefetch_related('reviews')


class ReviewCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, product_id):
        product = get_object_or_404(Product, id=product_id, is_active=True)
        if Review.objects.filter(product=product, author=request.user).exists():
            return Response({'detail': 'You have already reviewed this product.'}, status=status.HTTP_400_BAD_REQUEST)
        s = ReviewSerializer(data=request.data)
        s.is_valid(raise_exception=True)
        review = s.save(product=product, author=request.user)

        from core.emails import send_review_notification
        send_review_notification(product.seller, product, review)

        return Response(s.data, status=status.HTTP_201_CREATED)


class ReviewListView(generics.ListAPIView):
    serializer_class   = ReviewSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return Review.objects.filter(product_id=self.kwargs['product_id']).select_related('author')


class WishlistView(generics.ListAPIView):
    serializer_class   = WishlistSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Wishlist.objects.filter(user=self.request.user).select_related('product')


class WishlistToggleView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        obj, created = Wishlist.objects.get_or_create(user=request.user, product=product)
        if not created:
            obj.delete()
            return Response({'wishlisted': False})
        return Response({'wishlisted': True}, status=status.HTTP_201_CREATED)
    

class ProductDownloadView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        product = get_object_or_404(Product, pk=pk)

        has_purchased = OrderItem.objects.filter(
            product=product,
            order__buyer=request.user,
            order__status='completed'
        ).exists()

        if not has_purchased:
            return Response({'detail': 'You have not purchased this product.'}, status=status.HTTP_403_FORBIDDEN)

        if not product.file:
            return Response({'detail': 'No file available for this product yet.'}, status=status.HTTP_404_NOT_FOUND)

        filename = product.file.name.split('/')[-1]
        return FileResponse(product.file.open('rb'), as_attachment=True, filename=filename)