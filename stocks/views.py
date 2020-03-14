from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.response import Response

from stocks.models import StockCard, StockIn, ItemIn, StockOut, ItemOut
from stocks.serializers import StockCardSerializer, StockInSerializer, ItemInSerializer, StockOutSerializer, \
    ItemOutSerializer


class StockCardViewSet(viewsets.ModelViewSet):
    serializer_class = StockCardSerializer
    queryset = StockCard.objects.all()

    filterset_fields = [
        'numcode',
        'product',
        'is_publish',
    ]

    message = 'Not implemented for this action!'

    def create(self, request, *args, **kwargs):
        raise PermissionDenied(self.message)

    def update(self, request, *args, **kwargs):
        raise PermissionDenied(self.message)

    def partial_update(self, request, *args, **kwargs):
        raise PermissionDenied(self.message)

    def destroy(self, request, *args, **kwargs):
        raise PermissionDenied(self.message)


class StockInViewSet(viewsets.ModelViewSet):
    serializer_class = StockInSerializer
    queryset = StockIn.objects.all().order_by('-created')

    search_fields = [
        'supplier__name',
        'user__username',
        'user__email',
    ]

    filterset_fields = [
        'numcode',
        'supplier',
        'user',
        'is_init',
    ]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(methods=['POST'], detail=True)
    def calculate(self, request, pk=None):
        stock_in = self.get_object()
        if not stock_in.supplier:
            raise ValidationError({'detail': f'Supplier is not added'})
        item_ins = ItemIn.objects.filter(stockin=stock_in, is_init=False)
        if item_ins.exists():
            for item_in in item_ins:
                # if (item_in.product.stock - item_in.quantity) <= 0:
                #     raise ValidationError('Quantity not available in stock')
                #
                if item_in.quantity < 1:
                    raise ValidationError({'detail': f'Item {item_in.product.name} may not be zero.'})
                product = item_in.product
                product.stock = product.stock + item_in.quantity
                product.save()

            stock_in.is_calculate = True
            stock_in.save()
        else:
            raise ValidationError({'detail': 'Item cannot be empty.'})
        return Response(self.serializer_class(stock_in).data)


class ItemInViewSet(viewsets.ModelViewSet):
    serializer_class = ItemInSerializer
    queryset = ItemIn.objects.all()

    search_fields = [
        'stockin__numcode',
        'product__name',
    ]

    filterset_fields = [
        'stockin',
        'product',
        'is_init',
    ]


class StockOutViewSet(viewsets.ModelViewSet):
    serializer_class = StockOutSerializer
    queryset = StockOut.objects.all()

    search_fields = [
        'numcode',
        'customer',
        'user',
        'is_publish',
    ]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ItemOutViewSet(viewsets.ModelViewSet):
    serializer_class = ItemOutSerializer
    queryset = ItemOut.objects.all()

    search_fields = [
        'stockout',
        'product',
    ]
