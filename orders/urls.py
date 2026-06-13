from django.urls import path
from .views import OrderListView, OrderDetailView, CheckoutView, CouponValidateView, SellerOrdersView
from .payments import CreatePaymentIntentView

urlpatterns = [
    path('',              OrderListView.as_view(),      name='order-list'),
    path('<int:pk>/',     OrderDetailView.as_view(),    name='order-detail'),
    path('checkout/',     CheckoutView.as_view(),       name='checkout'),
    path('coupon/',       CouponValidateView.as_view(), name='coupon-validate'),
    path('seller-sales/', SellerOrdersView.as_view(),   name='seller-orders'),
    path('create-payment-intent/', CreatePaymentIntentView.as_view(), name='create-payment-intent'),
]