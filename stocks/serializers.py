from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from stocks.models import StockCard, StockIn, ItemIn, StockOut, ItemOut


class StockCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockCard
        fields = '__all__'


class StockInSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockIn
        fields = '__all__'
        read_only_fields = [
            'numcode',
            'user',
            'is_publish',
        ]


class ItemInSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemIn
        fields = '__all__'
        validators = [
            UniqueTogetherValidator(
                queryset=ItemIn.objects.all(),
                fields=['product', 'stockin'],
            )
        ]


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
