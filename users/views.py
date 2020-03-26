from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
from django.http import HttpResponse
from rest_framework import viewsets
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from users.filters import CustomerFilter, SupplierFilter
from users.models import Customer, Supplier
from users.serializers import UserSerializer, CustomerSerializer, SupplierSerializer, SigninSerializer
from utils.pdf import TOCSV, TOPDF


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

    def destroy(self, request, *args, **kwargs):
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
                    'user_id': user.pk,
                    'email': user.email,
                    'token': f'Token {token.key}'
                }

                return Response(data)

            except User.DoesNotExist:
                raise ValidationError({'detail': 'Username not found'})
            except Token.DoesNotExist:
                raise ValidationError({'detail': 'Token not initialize for this user'})


# @method_decorator(cache_page(60 * 5), name='dispatch')
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

    @action(methods=['POST', 'GET'], detail=False)
    def export_csv(self, request, pk=None):
        response = HttpResponse(content_type='application/csv')
        response['Content-Disposition'] = 'attachment; filename=somefilename.csv'
        queryset = self.filter_queryset(self.get_queryset().filter(is_init=False))

        header = [
            'Nomer Pelanggan',
            'Nama Pelanggan',
            'Kontak Pelanggan',
            'Alamat Pelanggan'
        ]

        csv = TOCSV(header, [[
            obj.numcode,
            obj.name,
            obj.phone,
            obj.address
        ] for obj in queryset], response)

        return csv.build()

    @action(methods=['POST', 'GET'], detail=False)
    def export_pdf(self, request, pk=None):
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename=somefilename.pdf'
        queryset = self.filter_queryset(self.get_queryset().filter(is_init=False))

        pdf = TOPDF(response, 'Laporan Pelanggan', None)
        pdf.set_table_detail([
            pdf.set_subject('Laporan Pelanggan'),
            pdf.set_periode(request),
            pdf.set_user(request),
            pdf.set_date_created()
        ])
        pdf.set_break()

        temp = []
        number = 1
        header = [
            '#',
            'Nomer Pelanggan',
            'Nama Pelanggan',
            'Kontak Pelanggan',
            'Alamat Pelanggan',
        ]

        for obj in queryset:
            temp.append([
                number,
                obj.numcode,
                obj.name,
                obj.phone,
                obj.address
            ])
            number += 1
        pdf.set_table(header, temp, 'LEFT', None)
        return pdf.build()


# @method_decorator(cache_page(60 * 5), name='dispatch')
class SupplierViewSet(viewsets.ModelViewSet):
    serializer_class = SupplierSerializer
    queryset = Supplier.objects.all().order_by('-created')

    search_fields = [
        'numcode',
        'name',
        'phone',
        'address',
    ]

    filterset_class = SupplierFilter

    @action(methods=['POST', 'GET'], detail=False)
    def export_csv(self, request, pk=None):
        response = HttpResponse(content_type='application/csv')
        response['Content-Disposition'] = 'attachment; filename=somefilename.csv'
        queryset = self.filter_queryset(self.get_queryset().filter(is_init=False))

        header = [
            'Nomer Supplier',
            'Nama Supplier',
            'Kontak Supplier',
            'Alamat Supplier'
        ]

        csv = TOCSV(header, [[
            obj.numcode,
            obj.name,
            obj.phone,
            obj.address
        ] for obj in queryset], response)

        return csv.build()

    @action(methods=['POST', 'GET'], detail=False)
    def export_pdf(self, request, pk=None):
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename=somefilename.pdf'
        queryset = self.filter_queryset(self.get_queryset().filter(is_init=False))

        pdf = TOPDF(response, 'Laporan Supplier', None)
        pdf.set_table_detail([
            pdf.set_subject('Laporan Supplier'),
            pdf.set_periode(request),
            pdf.set_user(request),
            pdf.set_date_created()
        ])
        pdf.set_break()

        temp = []
        number = 1
        header = [
            '#',
            'Nomer Supplier',
            'Nama Supplier',
            'Kontak Supplier',
            'Alamat Supplier',
        ]

        for obj in queryset:
            temp.append([
                number,
                obj.numcode,
                obj.name,
                obj.phone,
                obj.address
            ])
            number += 1
        pdf.set_table(header, temp, 'LEFT', None)
        return pdf.build()
