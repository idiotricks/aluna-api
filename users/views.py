from django.contrib.auth.models import User
from rest_framework import viewsets, status
from rest_framework.decorators import action, permission_classes
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response

from users.models import Customer, Supplier
from users.serializers import UserSerializer, CustomerSerializer, SupplierSerializer


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    search_fields = [
        'email',
        'first_name',
        'last_name',
    ]

    filterset_fields = [
        'username',
        'is_superuser',
        'is_active',
        'is_staff',
    ]

    def create(self, request, *args, **kwargs):
        raise PermissionDenied('Resource not found')

    def update(self, request, *args, **kwargs):
        raise PermissionDenied('Resource not found')

    def destroy(self, request, *args, **kwargs):
        raise PermissionDenied('Resource not found')

    def partial_update(self, request, pk=None):
        raise PermissionDenied('Resource not found')


class CustomerViewSet(viewsets.ModelViewSet):
    serializer_class = CustomerSerializer
    queryset = Customer.objects.all().order_by('-created')

    search_fields = [
        'numcode',
        'name',
        'phone',
        'address',
    ]

    filterset_fields = [
        'numcode',
        'is_publish',
    ]

    @action(methods=['POST'], detail=True)
    def publish(self, request, pk=None):
        customer = self.get_object()
        customer.is_publish = True
        customer.save()

        return Response(self.serializer_class(customer).data)

    @action(methods=['POST'], detail=True)
    def draft(self, request, pk=None):
        customer = self.get_object()
        customer.is_publish = False
        customer.save()

        return Response(self.serializer_class(customer).data)


class SupplierViewSet(viewsets.ModelViewSet):
    serializer_class = SupplierSerializer
    queryset = Supplier.objects.all().order_by('-created')

    search_fields = [
        'name',
        'phone',
        'address',
    ]

    filterset_fields = [
        'numcode',
        'is_publish',
    ]

    @action(methods=['POST'], detail=True)
    def publish(self, request, pk=None):
        supplier = self.get_object()
        supplier.is_publish = True
        supplier.save()

        return Response(self.serializer_class(supplier).data)

    @action(methods=['POST'], detail=True)
    def draft(self, request, pk=None):
        supplier = self.get_object()
        supplier.is_publish = False
        supplier.save()

        return Response(self.serializer_class(supplier).data)
