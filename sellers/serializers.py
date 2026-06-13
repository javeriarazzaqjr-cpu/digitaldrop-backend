from rest_framework import serializers
from .models import SellerProfile


class SellerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model  = SellerProfile
        fields = ('id', 'store_name', 'store_slug', 'store_desc',
                  'payout_method', 'payout_account', 'min_payout',
                  'notify_sale', 'notify_review')
        read_only_fields = ('id',)