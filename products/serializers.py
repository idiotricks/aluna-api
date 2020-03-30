from django.db.models import Sum
from rest_framework import serializers

from products.models import Product


class ProductSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    stock_card = serializers.SerializerMethodField()

    def get_username(self, obj):
        if obj.user:
            return obj.user.username
        return '-'

    def get_stock_card(self, obj):
        if not obj.is_init:
            stock_cards = obj.productstockcard.all()
            queryset = stock_cards.aggregate(
                total_in=Sum('total_in'),
                total_out=Sum('total_out'),
                end_balance=Sum('total_in') - Sum('total_out')
            )

            return queryset
        return {'init_balance': None, 'total_in': None, 'total_out': None, 'end_balance': None}

    class Meta:
        model = Product
        fields = '__all__'
