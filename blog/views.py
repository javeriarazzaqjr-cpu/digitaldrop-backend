from rest_framework import generics, permissions
from .models import BlogPost
from .serializers import BlogPostListSerializer, BlogPostDetailSerializer


class BlogListView(generics.ListAPIView):
    queryset           = BlogPost.objects.filter(is_published=True)
    serializer_class   = BlogPostListSerializer
    permission_classes = [permissions.AllowAny]


class BlogDetailView(generics.RetrieveAPIView):
    queryset           = BlogPost.objects.filter(is_published=True)
    serializer_class   = BlogPostDetailSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field       = 'slug'