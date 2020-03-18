from rest_framework import viewsets

from products.filters import ProductFilter
from products.models import Product
from products.serializers import ProductSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    search_fields = [
        'numcode',
        'name',
        'user__username',
        'user__email',
        'cogs',
        'price',
    ]

    filterset_class = ProductFilter

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
