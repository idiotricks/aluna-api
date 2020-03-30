from rest_framework import serializers

from stocks.models import StockCard, StockIn, ItemIn, StockOut, ItemOut


class StockCardSerializer(serializers.ModelSerializer):
    product_name = serializers.SerializerMethodField()

    def get_product_name(self, obj):
        return obj.product.name

    class Meta:
        model = StockCard
        fields = '__all__'


class StockInSerializer(serializers.ModelSerializer):
    supplier_name = serializers.SerializerMethodField()
    supplier_phone = serializers.SerializerMethodField()
    total_quantity = serializers.SerializerMethodField()

    def get_total_quantity(self, obj):
        items = ItemIn.objects.filter(stockin=obj, is_init=False)
        total = 0
        for i in items:
            total += i.quantity
        return total

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

    def get_product_name(self, obj):
        if obj.product:
            return f'{obj.product.name} / {obj.product.numcode}'
        return ''

    def create(self, validated_data):
        itemins = ItemIn.objects.filter(
            is_init=False,
            stockin=validated_data.get('stockin'),
            product=validated_data.get('product')
        )

        if itemins.exists():
            instance = itemins.first()
            instance.quantity = instance.quantity + validated_data.get('quantity')
        else:
            instance = ItemIn.objects.create(**validated_data)

        instance.end_stock = instance.stock + instance.quantity
        instance.save()

        return instance

    def update(self, instance, validated_data):
        instance = super(ItemInSerializer, self).update(instance, validated_data)
        instance.end_stock = instance.stock + instance.quantity
        instance.save()
        return instance

    class Meta:
        model = ItemIn
        fields = '__all__'


class StockOutSerializer(serializers.ModelSerializer):
    customer_name = serializers.SerializerMethodField()
    customer_phone = serializers.SerializerMethodField()
    total_quantity = serializers.SerializerMethodField()

    def get_total_quantity(self, obj):
        items = ItemOut.objects.filter(stockout=obj, is_init=False)
        total = 0
        for i in items:
            total += i.quantity
        return total

    def get_customer_name(self, obj):
        if obj.customer:
            return obj.customer.name
        return '-'

    def get_customer_phone(self, obj):
        if obj.customer:
            return obj.customer.phone
        return '-'

    class Meta:
        model = StockOut
        fields = '__all__'
        read_only_fields = [
            'numcode',
            'user',
            'is_publish',
        ]


class ItemOutSerializer(serializers.ModelSerializer):
    product_name = serializers.SerializerMethodField()
    product_stock = serializers.SerializerMethodField()
    is_problem = serializers.SerializerMethodField()

    def get_product_name(self, obj):
        if obj.product:
            return f'{obj.product.name} / {obj.product.numcode}'

    def get_product_stock(self, obj):
        if obj.product:
            return obj.product.stock

    def get_is_problem(self, obj):
        if obj.quantity:
            data = obj.stock - obj.quantity
            if data < 0:
                return True
            return False
        return False

    def create(self, validated_data):
        itemouts = ItemOut.objects.filter(
            is_init=False,
            stockout=validated_data.get('stockout'),
            product=validated_data.get('product')
        )

        if itemouts.exists():
            instance = itemouts.first()
            instance.quantity = instance.quantity + validated_data.get('quantity')
        else:
            instance = ItemOut.objects.create(**validated_data)

        instance.end_stock = instance.stock - instance.quantity
        instance.save()

        return instance

    def update(self, instance, validated_data):
        instance = super(ItemOutSerializer, self).update(instance, validated_data)
        instance.end_stock = instance.stock - instance.quantity
        instance.save()
        return instance

    class Meta:
        model = ItemOut
        fields = '__all__'


#########################
# Reporting Serializers #
#########################

class StockCardReportingSerializer(serializers.Serializer):
    product__name = serializers.CharField()
    product__numcode = serializers.CharField()
    init_balance__sum = serializers.IntegerField()
    total_in__sum = serializers.IntegerField()
    total_out__sum = serializers.IntegerField()
    end_balance__sum = serializers.IntegerField()


class ItemInReportingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemOut
        fields = '__all__'
        depth = 1


class StockInReportingSerializer(serializers.ModelSerializer):
    stockinitemin = ItemInReportingSerializer(many=True)
    total_quantity = serializers.SerializerMethodField()

    def get_total_quantity(self, obj):
        items = ItemIn.objects.filter(stockin=obj, is_init=False)
        total = 0
        for i in items:
            total += i.quantity

        total = f'{total} unit'
        return total

    class Meta:
        model = StockIn
        fields = '__all__'
        depth = 1


class ItemOutReportingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemOut
        fields = '__all__'
        depth = 1


class StockOutReportingSerializer(serializers.ModelSerializer):
    stockoutitemout = ItemOutReportingSerializer(many=True)
    total_quantity = serializers.SerializerMethodField()

    def get_total_quantity(self, obj):
        items = ItemOut.objects.filter(stockout=obj, is_init=False)
        total = 0
        for i in items:
            total += i.quantity

        total = f'{total} unit'
        return total

    class Meta:
        model = StockOut
        fields = '__all__'
        depth = 1
