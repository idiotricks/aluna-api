from django.http import HttpResponse
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from products.filters import ProductFilter
from products.models import Product
from products.permissions import IsAccessDeleteProduct
from products.serializers import ProductSerializer
from utils.pdf import TOCSV, TOPDF


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    permission_classes = [
        IsAuthenticated,
        IsAccessDeleteProduct,
    ]
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

    @action(methods=['POST', 'GET'], detail=False)
    def export_csv(self, request, pk=None):
        response = HttpResponse(content_type='application/csv')
        response['Content-Disposition'] = 'attachment; filename=somefilename.csv'
        queryset = self.filter_queryset(self.get_queryset().filter(is_init=False))

        header = [
            'Nomer Produk',
            'Nama Produk',
            'Harga Beli',
            'Harga Jual',
            'Stok'
        ]

        csv = TOCSV(header, [[
            obj.numcode,
            obj.name,
            obj.cogs,
            obj.price,
            obj.stock,
        ] for obj in queryset], response)

        return csv.build()

    @action(methods=['POST', 'GET'], detail=False)
    def export_pdf(self, request, pk=None):
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename=somefilename.pdf'
        queryset = self.filter_queryset(self.get_queryset().filter(is_init=False))

        pdf = TOPDF(response, 'Laporan Produk', None)
        pdf.set_table_detail([
            pdf.set_subject('Laporan Produk'),
            pdf.set_periode(request),
            pdf.set_user(request),
            pdf.set_date_created()
        ])
        pdf.set_break()

        temp = []
        number = 1
        header = [
            '#',
            'Nomer Produk',
            'Nama Produk',
            'Harga Beli',
            'Harga Jual',
            'Stok'
        ]

        for obj in queryset:
            temp.append([
                number,
                obj.numcode,
                obj.name,
                obj.cogs,
                obj.price,
                obj.stock,
            ])
            number += 1

        pdf.set_table(header, temp, 'LEFT', None)
        return pdf.build()
