from django.urls import path
from .views import (
    RegisterView, LoginView, LogoutView, MeView, ChangePasswordView,
    PasswordResetRequestView, PasswordResetConfirmView,
)

urlpatterns = [
    path('register/',        RegisterView.as_view(),             name='auth-register'),
    path('login/',           LoginView.as_view(),                name='auth-login'),
    path('logout/',          LogoutView.as_view(),               name='auth-logout'),
    path('me/',              MeView.as_view(),                   name='auth-me'),
    path('change-password/', ChangePasswordView.as_view(),       name='auth-change-password'),
    path('password-reset/',  PasswordResetRequestView.as_view(), name='password-reset'),
    path('password-reset-confirm/', PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
]