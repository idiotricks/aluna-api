from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from stocks.models import StockCard, StockIn, ItemIn, StockOut, ItemOut


class StockCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockCard
        fields = '__all__'


class StockInSerializer(serializers.ModelSerializer):
    supplier_name = serializers.SerializerMethodField()
    supplier_phone = serializers.SerializerMethodField()

    def get_supplier_name(self, obj):
        if obj.supplier:
            return obj.supplier.name
        return '-'

    def get_supplier_phone(self, obj):
        if obj.supplier:
            return obj.supplier.phone
        return '-'

    class Meta:
        model = StockIn
        fields = '__all__'
        read_only_fields = [
            'numcode',
            'user',
            'is_publish',
        ]


class ItemInSerializer(serializers.ModelSerializer):
    product_name = serializers.SerializerMethodField()
    product_stock = serializers.SerializerMethodField()
    residual_stock = serializers.SerializerMethodField()
    buffer_stock = serializers.SerializerMethodField()

    def get_product_name(self, obj):
        if obj.product:
            return f'{obj.product.name}/{obj.product.numcode}'

    def get_product_stock(self, obj):
        if obj.product:
            return obj.product.stock

    def get_residual_stock(self, obj):
        if obj.product:
            if obj.quantity:
                data = obj.product.stock - obj.quantity
                if data > 0:
                    return data
                return 0
        return 0

    def get_buffer_stock(self, obj):
        if obj.product:
            if obj.quantity:
                data = obj.product.stock - obj.quantity
                if data < 0:
                    return abs(data)
                return 0
        return 0

    class Meta:
        model = ItemIn
        fields = '__all__'


class StockOutSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockOut
        fields = '__all__'
        read_only_fields = [
            'numcode',
            'user',
            'is_publish',
        ]


class ItemOutSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemOut
        fields = '__all__'
        validators = [
            UniqueTogetherValidator(
                queryset=ItemOut.objects.all(),
                fields=['product', 'stockout'],
            )
        ]
