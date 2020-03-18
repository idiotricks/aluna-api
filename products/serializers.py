from rest_framework import serializers

from products.models import Product


class ProductSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()

    def get_username(self, obj):
        if obj.user:
            return obj.user.username
        return '-'

    class Meta:
        model = Product
        fields = '__all__'
