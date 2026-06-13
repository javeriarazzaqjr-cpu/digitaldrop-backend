from django.urls import path
from .views import SellerProfileView, SellerPublicView, SellerDashboardView

urlpatterns = [
    path('profile/',       SellerProfileView.as_view(),   name='seller-profile'),
    path('dashboard/',     SellerDashboardView.as_view(), name='seller-dashboard'),
    path('<int:user_id>/', SellerPublicView.as_view(),    name='seller-public'),
]