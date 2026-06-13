from django.db import models
from django.conf import settings


class BlogPost(models.Model):
    title        = models.CharField(max_length=300)
    slug         = models.SlugField(unique=True, max_length=300)
    category     = models.CharField(max_length=80)
    emoji        = models.CharField(max_length=10, blank=True)
    image_url    = models.URLField(blank=True)
    excerpt      = models.TextField()
    content      = models.TextField()
    author       = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
                                     null=True, related_name='blog_posts')
    read_time    = models.CharField(max_length=20, default='5 min')
    is_published = models.BooleanField(default=True)
    published_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-published_at']

    def __str__(self):
        return self.title