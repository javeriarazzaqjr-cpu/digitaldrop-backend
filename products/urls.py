from django.urls import path
from .views import (
    CategoryListView, ProductListView, ProductDetailView,
    ProductCreateView, ProductUpdateDeleteView, MyProductsView,
    ReviewCreateView, ReviewListView, WishlistView, WishlistToggleView,
)

urlpatterns = [
    path('',                           ProductListView.as_view(),        name='product-list'),
    path('create/',                    ProductCreateView.as_view(),      name='product-create'),
    path('mine/',                      MyProductsView.as_view(),         name='my-products'),
    path('<int:pk>/',                  ProductDetailView.as_view(),      name='product-detail'),
    path('<int:pk>/edit/',             ProductUpdateDeleteView.as_view(),name='product-edit'),
    path('<int:product_id>/reviews/',  ReviewListView.as_view(),         name='review-list'),
    path('<int:product_id>/review/',   ReviewCreateView.as_view(),       name='review-create'),
    path('categories/',                CategoryListView.as_view(),       name='category-list'),
    path('wishlist/',                  WishlistView.as_view(),           name='wishlist'),
    path('<int:product_id>/wishlist/', WishlistToggleView.as_view(),     name='wishlist-toggle'),
]