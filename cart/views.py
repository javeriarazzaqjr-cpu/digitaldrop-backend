from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import serializers
from django.shortcuts import get_object_or_404

from .models import CartItem
from products.models import Product
from products.serializers import ProductListSerializer


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductListSerializer(read_only=True)

    class Meta:
        model  = CartItem
        fields = ('id', 'product', 'added_at')


class CartListView(generics.ListAPIView):
    serializer_class   = CartItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return CartItem.objects.filter(user=self.request.user).select_related('product__category')


class CartAddView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, product_id):
        product = get_object_or_404(Product, id=product_id, is_active=True)
        item, created = CartItem.objects.get_or_create(user=request.user, product=product)
        if not created:
            return Response({'detail': 'Already in cart.'}, status=status.HTTP_200_OK)
        return Response(CartItemSerializer(item).data, status=status.HTTP_201_CREATED)


class CartRemoveView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, product_id):
        CartItem.objects.filter(user=request.user, product_id=product_id).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CartClearView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request):
        CartItem.objects.filter(user=request.user).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CartSummaryView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        items    = CartItem.objects.filter(user=request.user).select_related('product')
        subtotal = sum(i.product.price for i in items)
        return Response({
            'items':    CartItemSerializer(items, many=True, context={'request': request}).data,
            'count':    items.count(),
            'subtotal': float(subtotal),
        })