from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from core.emails import send_welcome_email

from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from core.emails import send_welcome_email, send_password_reset_email

from .models import User
from .serializers import (
    RegisterSerializer, LoginSerializer, UserSerializer,
    ChangePasswordSerializer, get_tokens_for_user
)


class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        s = RegisterSerializer(data=request.data)
        s.is_valid(raise_exception=True)
        user = s.save()
        send_welcome_email(user)  # ← add this line
        tokens = get_tokens_for_user(user)
        return Response({
            'user':   UserSerializer(user).data,
            'tokens': tokens,
        }, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        s = LoginSerializer(data=request.data)
        s.is_valid(raise_exception=True)
        user   = s.validated_data['user']
        tokens = get_tokens_for_user(user)
        return Response({
            'user':   UserSerializer(user).data,
            'tokens': tokens,
        })


class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            refresh = RefreshToken(request.data['refresh'])
            refresh.blacklist()
            return Response({'detail': 'Logged out successfully.'})
        except Exception:
            return Response({'detail': 'Invalid token.'}, status=status.HTTP_400_BAD_REQUEST)


class MeView(generics.RetrieveUpdateAPIView):
    serializer_class   = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class ChangePasswordView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        s = ChangePasswordSerializer(data=request.data, context={'request': request})
        s.is_valid(raise_exception=True)
        s.save()
        return Response({'detail': 'Password updated successfully.'})
    

class PasswordResetRequestView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = request.data.get('email', '').strip()
        try:
            user = User.objects.get(email=email)
            uid   = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            reset_link = f'http://localhost:3000/dp.html#reset_uid={uid}&reset_token={token}'
            send_password_reset_email(user, reset_link)
        except User.DoesNotExist:
            pass
        return Response({'detail': 'If that email exists, a reset link has been sent.'})


class PasswordResetConfirmView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        uid      = request.data.get('uid', '')
        token    = request.data.get('token', '')
        password = request.data.get('password', '')
        try:
            pk   = force_str(urlsafe_base64_decode(uid))
            user = User.objects.get(pk=pk)
            if not default_token_generator.check_token(user, token):
                return Response({'detail': 'Invalid or expired link.'}, status=status.HTTP_400_BAD_REQUEST)
            user.set_password(password)
            user.save()
            return Response({'detail': 'Password reset successfully.'})
        except Exception:
            return Response({'detail': 'Invalid reset link.'}, status=status.HTTP_400_BAD_REQUEST)