from django.urls import path
from .views import CartListView, CartAddView, CartRemoveView, CartClearView, CartSummaryView

urlpatterns = [
    path('',                         CartListView.as_view(),    name='cart-list'),
    path('summary/',                 CartSummaryView.as_view(), name='cart-summary'),
    path('clear/',                   CartClearView.as_view(),   name='cart-clear'),
    path('add/<int:product_id>/',    CartAddView.as_view(),     name='cart-add'),
    path('remove/<int:product_id>/', CartRemoveView.as_view(),  name='cart-remove'),
]