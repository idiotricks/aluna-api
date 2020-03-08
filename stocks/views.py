from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied

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
    queryset = StockIn.objects.all()

    search_fields = [
        'supplier__name',
        'user__username',
        'user__email',
    ]

    filterset_fields = [
        'numcode',
        'supplier',
        'user',
        'is_publish',
    ]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ItemInViewSet(viewsets.ModelViewSet):
    serializer_class = ItemInSerializer
    queryset = ItemIn.objects.all()

    search_fields = [
        'stockin',
        'product',
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
