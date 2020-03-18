from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from users.filters import CustomerFilter
from users.models import Customer, Supplier
from users.serializers import UserSerializer, CustomerSerializer, SupplierSerializer, SigninSerializer


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

    @action(methods=['POST'], detail=False, permission_classes=[AllowAny])
    def signin(self, request, pk=None):
        serializer = SigninSerializer(data=request.data)
        if serializer.is_valid():
            try:
                user = User.objects.get(username=serializer.data.get('username'))
                pwd_valid = check_password(serializer.data.get('password'), user.password)

                if not user.is_active:
                    raise ValidationError({'detail': 'User not activated'})

                if not pwd_valid:
                    raise ValidationError({'detail': 'Password not match'})

                token = Token.objects.get(user=user)
                data = {
                    'username': user.username,
                    'email': user.email,
                    'token': f'Token {token.key}'
                }

                return Response(data)

            except User.DoesNotExist:
                raise ValidationError({'detail': 'Username not found'})
            except Token.DoesNotExist:
                raise ValidationError({'detail': 'Token not initialize for this user'})


class CustomerViewSet(viewsets.ModelViewSet):
    serializer_class = CustomerSerializer
    queryset = Customer.objects.all().order_by('-created')

    search_fields = [
        'numcode',
        'name',
        'phone',
        'address',
    ]

    filterset_class = CustomerFilter


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
        'is_init',
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
