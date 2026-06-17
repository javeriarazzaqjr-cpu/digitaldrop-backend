from rest_framework import serializers
from .models import Category, Product, ProductInclude, Review, Wishlist


class CategorySerializer(serializers.ModelSerializer):
    product_count = serializers.IntegerField(source='products.count', read_only=True)

    class Meta:
        model  = Category
        fields = ('id', 'name', 'emoji', 'slug', 'product_count')


class ProductIncludeSerializer(serializers.ModelSerializer):
    class Meta:
        model  = ProductInclude
        fields = ('id', 'item', 'order')


class ReviewSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.full_name', read_only=True)

    class Meta:
        model  = Review
        fields = ('id', 'author_name', 'rating', 'text', 'created_at')
        read_only_fields = ('id', 'author_name', 'created_at')

    def validate_rating(self, value):
        if not (1 <= value <= 5):
            raise serializers.ValidationError('Rating must be between 1 and 5.')
        return value


class ProductListSerializer(serializers.ModelSerializer):
    category_name    = serializers.CharField(source='category.name', read_only=True)
    seller_name      = serializers.CharField(source='seller.full_name', read_only=True)
    avg_rating       = serializers.ReadOnlyField()
    review_count     = serializers.ReadOnlyField()
    discount_percent = serializers.ReadOnlyField()
    is_wishlisted    = serializers.SerializerMethodField()

    class Meta:
        model  = Product
        fields = (
            'id', 'name', 'description', 'price', 'old_price',
            'category_name', 'seller_name', 'seller_id',
            'emoji', 'badge', 'tags', 'image',
            'avg_rating', 'review_count', 'discount_percent',
            'sales_count', 'is_active', 'created_at', 'is_wishlisted',
        )

    def get_is_wishlisted(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return Wishlist.objects.filter(user=request.user, product=obj).exists()
        return False


class ProductDetailSerializer(ProductListSerializer):
    includes = ProductIncludeSerializer(many=True, read_only=True)
    reviews  = ReviewSerializer(many=True, read_only=True)

    class Meta(ProductListSerializer.Meta):
        fields = ProductListSerializer.Meta.fields + ('includes', 'reviews')


class ProductCreateSerializer(serializers.ModelSerializer):
    includes = serializers.ListField(
        child=serializers.CharField(max_length=200),
        write_only=True, required=False
    )

    class Meta:
        model  = Product
        fields = ('name', 'description', 'category', 'price', 'old_price',
                  'emoji', 'badge', 'tags', 'includes', 'file', 'image')
    def create(self, validated_data):
        includes_data = validated_data.pop('includes', [])
        product = Product.objects.create(**validated_data)
        for i, item in enumerate(includes_data):
            ProductInclude.objects.create(product=product, item=item, order=i)
        return product

    def update(self, instance, validated_data):
        includes_data = validated_data.pop('includes', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if includes_data is not None:
            instance.includes.all().delete()
            for i, item in enumerate(includes_data):
                ProductInclude.objects.create(product=instance, item=item, order=i)
        return instance


class WishlistSerializer(serializers.ModelSerializer):
    product = ProductListSerializer(read_only=True)

    class Meta:
        model  = Wishlist
        fields = ('id', 'product', 'added_at')