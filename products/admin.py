from django.contrib import admin
from .models import Category, Product, ProductInclude, Review

class ProductIncludeInline(admin.TabularInline):
    model = ProductInclude
    extra = 1

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display  = ('name', 'seller', 'category', 'price', 'sales_count', 'is_active')
    list_filter   = ('category', 'badge', 'is_active')
    search_fields = ('name', 'seller__email')
    inlines       = [ProductIncludeInline]

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'emoji', 'slug')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'author', 'rating', 'created_at')