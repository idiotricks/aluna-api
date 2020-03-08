from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from products.models import Product
from products.serializers import ProductSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    search_fields = [
        'name',
        'user__username',
        'user__email',
    ]

    filterset_fields = [
        'numcode',
        'user',
        'is_publish',
    ]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(methods=['POST'], detail=True)
    def publish(self, request, pk=None):
        product = self.get_object()
        product.is_publish = True
        product.save()

        return Response(self.serializer_class(product).data)

    @action(methods=['POST'], detail=True)
    def draft(self, request, pk=None):
        product = self.get_object()
        product.is_publish = False
        product.save()

        return Response(self.serializer_class(product).data)
