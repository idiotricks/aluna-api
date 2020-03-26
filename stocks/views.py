from django.db.models import Sum
from django.http import HttpResponse
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.response import Response

from stocks.filters import StockInFilter, StockOutFilter, StockCardFilter
from stocks.models import StockCard, StockIn, ItemIn, StockOut, ItemOut
from stocks.serializers import StockCardSerializer, StockInSerializer, ItemInSerializer, StockOutSerializer, \
    ItemOutSerializer
from utils.pdf import TOPDF, TOCSV


class StockCardViewSet(viewsets.ModelViewSet):
    serializer_class = StockCardSerializer
    queryset = StockCard.objects.all()

    search_fields = [
        'numcode',
        'product__name',
    ]

    filterset_class = StockCardFilter

    message = 'Not implemented for this action!'

    def create(self, request, *args, **kwargs):
        raise PermissionDenied(self.message)

    def update(self, request, *args, **kwargs):
        raise PermissionDenied(self.message)

    def partial_update(self, request, *args, **kwargs):
        raise PermissionDenied(self.message)

    def destroy(self, request, *args, **kwargs):
        raise PermissionDenied(self.message)

    @action(methods=['POST', 'GET'], detail=False)
    def export_csv(self, request, pk=None):
        response = HttpResponse(content_type='application/csv')
        response['Content-Disposition'] = 'attachment; filename=somefilename.csv'
        queryset = self.filter_queryset(self.get_queryset().filter(is_init=False))
        queryset = queryset.values(
            'product__name',
            'product__numcode',
            'date',
        ).annotate(
            Sum('init_balance'),
            Sum('total_in'),
            Sum('total_out'),
            Sum('end_balance')
        ).order_by('-date')

        temp = []
        header = [
            'Nomer Produk',
            'Nama Produk',
            'Tanggal',
            'Saldo Awal',
            'Stok Masuk',
            'Stok Keluar',
            'Stok Akhir'
        ]
        for obj in queryset:
            temp.append([
                obj.get('product__numcode'),
                obj.get('product__name'),
                obj.get('date'),
                obj.get('init_balance__sum'),
                obj.get('total_in__sum'),
                obj.get('total_out__sum'),
                obj.get('end_balance__sum'),
            ])

        csv = TOCSV(header, temp, response)
        return csv.build()

    @action(methods=['POST', 'GET'], detail=False)
    def export_pdf(self, request, pk=None):
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename=somefilename.pdf'
        queryset = self.filter_queryset(self.get_queryset().filter(is_init=False))
        queryset = queryset.values(
            'product__name',
            'product__numcode',
            'date',
        ).annotate(
            Sum('init_balance'),
            Sum('total_in'),
            Sum('total_out'),
            Sum('end_balance')
        ).order_by('-date')

        pdf = TOPDF(response, 'Laporan Kartu Stok Barang', None)
        pdf.set_table_detail([
            pdf.set_subject('Laporan Kartu Stok'),
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
            'Tanggal',
            'Saldo Awal',
            'Stok Masuk',
            'Stok Keluar',
            'Stok Akhir'
        ]
        for obj in queryset:
            temp.append([
                number,
                obj.get('product__numcode'),
                obj.get('product__name'),
                obj.get('date'),
                obj.get('init_balance__sum'),
                obj.get('total_in__sum'),
                obj.get('total_out__sum'),
                obj.get('end_balance__sum'),
            ])
            number += 1
        pdf.set_table(header, temp, 'LEFT', None)
        return pdf.build()


class StockInViewSet(viewsets.ModelViewSet):
    serializer_class = StockInSerializer
    queryset = StockIn.objects.all().order_by('-created')

    search_fields = [
        'numcode',
        'supplier__name',
        'user__username',
        'user__email',
    ]

    filterset_class = StockInFilter

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(methods=['POST'], detail=True)
    def calculate(self, request, pk=None):
        stock_in = self.get_object()
        if not stock_in.supplier:
            raise ValidationError({'detail': f'Supplier is not added'})

        item_ins = ItemIn.objects.filter(stockin=stock_in, is_init=False)
        stock_cards = []
        if item_ins.exists():
            for item_in in item_ins:
                if item_in.quantity < 1:
                    raise ValidationError({'detail': f'Item {item_in.product.name} may not be zero.'})

                stock_cards.append(StockCard(
                    numcode=stock_in.numcode,
                    date=stock_in.date,
                    product=item_in.product,
                    init_balance=item_in.product.stock,
                    total_in=item_in.quantity,
                    end_balance=item_in.quantity + item_in.product.stock,
                    is_init=False
                ))
                product = item_in.product
                product.stock = product.stock + item_in.quantity
                product.save()

            stock_in.is_calculate = True
            stock_in.save()
            StockCard.objects.bulk_create(stock_cards)

        else:
            raise ValidationError({'detail': 'Item cannot be empty.'})
        return Response(self.serializer_class(stock_in).data)

    @action(methods=['POST', 'GET'], detail=False)
    def export_csv(self, request, pk=None):
        response = HttpResponse(content_type='application/csv')
        response['Content-Disposition'] = 'attachment; filename=somefilename.csv'
        queryset = self.filter_queryset(self.get_queryset().filter(is_calculate=True, is_init=False))

        queryset = queryset.prefetch_related('stockinitemin').values(
            'numcode',
            'supplier',
            'supplier__name',
            'supplier__numcode',
            'supplier__phone',
            'stockinitemin__product__numcode',
            'stockinitemin__product__name',
            'date',
        ).annotate(Sum('stockinitemin__quantity'))
        data = []
        header = [
            'Kode Stok',
            'Tanggal',
            'Kode Supplier',
            'Nama Supplier',
            'Kontak Supplier',
            'Kode Produk',
            'Produk',
            'Stok Masuk',
        ]

        for obj in queryset:
            data.append([
                obj.get('numcode'),
                obj.get('date'),
                obj.get('supplier__numcode'),
                obj.get('supplier__name'),
                obj.get('supplier__phone'),
                obj.get('stockinitemin__product__numcode'),
                obj.get('stockinitemin__product__name'),
                obj.get('stockinitemin__quantity__sum'),
            ])

        csv = TOCSV(header, data, response)
        return csv.build()

    @action(methods=['POST', 'GET'], detail=False)
    def export_pdf(self, request, pk=None):
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename=somefilename.pdf'
        queryset = self.filter_queryset(self.get_queryset().filter(is_calculate=True, is_init=False))
        queryset = queryset.prefetch_related('stockinitemin')

        pdf = TOPDF(response, 'Laporan Barang Masuk', None)
        for obj in queryset:
            temp_detail = []
            temp_detail += [
                pdf.set_subject(f'Laporan Stok Masuk {obj.numcode}'),
                pdf.set_periode(request),
                pdf.set_user(request),
                pdf.set_date_created(),
            ]

            temp = []
            header = [
                'Nomer Produk',
                'Nama Produk',
                'Stok Masuk'
            ]
            items = obj.stockinitemin.values(
                'product__numcode',
                'product__name',
            ).annotate(Sum('quantity'))
            total = obj.stockinitemin.aggregate(Sum('quantity'))

            for item in items:
                temp.append([
                    item.get('product__numcode'),
                    item.get('product__name'),
                    item.get('quantity__sum'),
                ])

            temp_detail += [
                pdf.set_other('Nomer Stok Masuk', obj.numcode),
                pdf.set_other('Tanggal', obj.date),
                pdf.set_other('Nomer Supplier', obj.supplier.numcode),
                pdf.set_other('Supplier', obj.supplier.name),
                pdf.set_other('Kontak Supplier', obj.supplier.phone),
                pdf.set_other('Total Stok Masuk', total.get('quantity__sum')),
            ]
            pdf.set_table_detail(temp_detail)
            pdf.set_break(0.2, 0.2)

            pdf.set_table(header, temp, 'LEFT', None)
            pdf.set_page_break()
        return pdf.build()

    @action(methods=['GET'], detail=True)
    def print_pdf(self, request, pk=None):
        obj = self.get_object()
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename=somefilename.pdf'

        pdf = TOPDF(response, 'Laporan Barang Masuk', None)
        temp_detail = []
        temp_detail += [
            pdf.set_subject(f'Laporan Stok Masuk {obj.numcode}'),
            pdf.set_periode(request),
            pdf.set_user(request),
            pdf.set_date_created(),
        ]

        temp = []
        header = [
            'Nomer Produk',
            'Nama Produk',
            'Stok Masuk'
        ]
        items = obj.stockinitemin.values(
            'product__numcode',
            'product__name',
        ).annotate(Sum('quantity'))
        total = obj.stockinitemin.aggregate(Sum('quantity'))

        for item in items:
            temp.append([
                item.get('product__numcode'),
                item.get('product__name'),
                item.get('quantity__sum'),
            ])

        temp_detail += [
            pdf.set_other('Nomer Stok Masuk', obj.numcode),
            pdf.set_other('Tanggal', obj.date),
            pdf.set_other('Nomer Supplier', obj.supplier.numcode),
            pdf.set_other('Supplier', obj.supplier.name),
            pdf.set_other('Kontak Supplier', obj.supplier.phone),
            pdf.set_other('Total Stok Masuk', total.get('quantity__sum')),
        ]
        pdf.set_table_detail(temp_detail)
        pdf.set_break(0.2, 0.2)

        pdf.set_table(header, temp, 'LEFT', None)
        pdf.set_page_break()
        return pdf.build()


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
        'customer__name',
        'user__username',
        'user__email',
    ]

    filterset_class = StockOutFilter

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(methods=['POST'], detail=True)
    def calculate(self, request, pk=None):
        stock_out = self.get_object()

        if not stock_out.customer:
            raise ValidationError({'detail': f'Customer is not added'})

        item_outs = ItemOut.objects.filter(stockout=stock_out, is_init=False)
        stock_cards = []
        if item_outs.exists():
            for item_out in item_outs:
                if not item_out.product:
                    raise ValidationError({'detail': f'one item does not have a product.'})

                if item_out.product.stock - item_out.quantity < 0:
                    raise ValidationError({'detail': f'product stock does not meet.'})

                if item_out.quantity < 1:
                    raise ValidationError({'detail': f'Item {item_out.product.name} may not be zero.'})

                # Stock Cards
                stock_cards.append(StockCard(
                    numcode=stock_out.numcode,
                    date=stock_out.date,
                    product=item_out.product,
                    init_balance=item_out.product.stock,
                    total_out=item_out.quantity,
                    end_balance=item_out.product.stock - item_out.quantity,
                    is_init=False
                ))

                product = item_out.product
                product.stock = product.stock - item_out.quantity
                product.save()
                StockCard.objects.bulk_create(stock_cards)

            stock_out.is_calculate = True
            stock_out.save()
        else:
            raise ValidationError({'detail': 'Item cannot be empty.'})

        return Response(self.serializer_class(stock_out).data)

    @action(methods=['POST', 'GET'], detail=False)
    def export_csv(self, request, pk=None):
        response = HttpResponse(content_type='application/csv')
        response['Content-Disposition'] = 'attachment; filename=somefilename.csv'
        queryset = self.filter_queryset(self.get_queryset().filter(is_calculate=True, is_init=False))

        queryset = queryset.prefetch_related('stockoutitemout').values(
            'numcode',
            'customer',
            'customer__name',
            'customer__numcode',
            'customer__phone',
            'stockoutitemout__product__numcode',
            'stockoutitemout__product__name',
            'date',
        ).annotate(Sum('stockoutitemout__quantity'))
        data = []
        header = [
            'Kode Stok',
            'Tanggal',
            'Kode Pelanggan',
            'Nama Pelanggan',
            'Kontak Pelanggan',
            'Kode Produk',
            'Produk',
            'Stok Keluar',
        ]

        for obj in queryset:
            data.append([
                obj.get('numcode'),
                obj.get('date'),
                obj.get('customer__numcode'),
                obj.get('customer__name'),
                obj.get('customer__phone'),
                obj.get('stockoutitemout__product__numcode'),
                obj.get('stockoutitemout__product__name'),
                obj.get('stockoutitemout__quantity__sum'),
            ])

        csv = TOCSV(header, data, response)
        return csv.build()

    @action(methods=['POST', 'GET'], detail=False)
    def export_pdf(self, request, pk=None):
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename=somefilename.pdf'
        queryset = self.filter_queryset(self.get_queryset().filter(is_calculate=True, is_init=False))
        queryset = queryset.prefetch_related('stockoutitemout')

        pdf = TOPDF(response, 'Laporan Barang Keluar', None)
        for obj in queryset:
            temp_detail = []
            temp_detail += [
                pdf.set_subject(f'Laporan Stok Keluar {obj.numcode}'),
                pdf.set_periode(request),
                pdf.set_user(request),
                pdf.set_date_created(),
            ]

            temp = []
            header = [
                'Nomer Produk',
                'Nama Produk',
                'Stok Keluar'
            ]
            items = obj.stockoutitemout.values(
                'product__numcode',
                'product__name',
            ).annotate(Sum('quantity'))
            total = obj.stockoutitemout.aggregate(Sum('quantity'))

            for item in items:
                temp.append([
                    item.get('product__numcode'),
                    item.get('product__name'),
                    item.get('quantity__sum'),
                ])

            temp_detail += [
                pdf.set_other('Nomer Stok Keluar', obj.numcode),
                pdf.set_other('Tanggal', obj.date),
                pdf.set_other('Nomer Pelanggan', obj.customer.numcode),
                pdf.set_other('Pelanggan', obj.customer.name),
                pdf.set_other('Kontak Supplier', obj.customer.phone),
                pdf.set_other('Total Stok Keluar', total.get('quantity__sum')),
            ]
            pdf.set_table_detail(temp_detail)
            pdf.set_break(0.2, 0.2)

            pdf.set_table(header, temp, 'LEFT', None)
            pdf.set_page_break()
        return pdf.build()

    @action(methods=['GET'], detail=True)
    def print_pdf(self, request, pk=None):
        obj = self.get_object()
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename=somefilename.pdf'

        pdf = TOPDF(response, 'Laporan Barang Keluar', None)
        temp_detail = []
        temp_detail += [
            pdf.set_subject(f'Laporan Stok Keluar {obj.numcode}'),
            pdf.set_periode(request),
            pdf.set_user(request),
            pdf.set_date_created(),
        ]

        temp = []
        header = [
            'Nomer Produk',
            'Nama Produk',
            'Stok Masuk'
        ]
        items = obj.stockoutitemout.values(
            'product__numcode',
            'product__name',
        ).annotate(Sum('quantity'))
        total = obj.stockoutitemout.aggregate(Sum('quantity'))

        for item in items:
            temp.append([
                item.get('product__numcode'),
                item.get('product__name'),
                item.get('quantity__sum'),
            ])

        temp_detail += [
            pdf.set_other('Nomer Stok Keluar', obj.numcode),
            pdf.set_other('Tanggal', obj.date),
            pdf.set_other('Nomer Pelanggan', obj.customer.numcode),
            pdf.set_other('Pelanggan', obj.customer.name),
            pdf.set_other('Kontak Pelanggan', obj.customer.phone),
            pdf.set_other('Total Stok Keluar', total.get('quantity__sum')),
        ]
        pdf.set_table_detail(temp_detail)
        pdf.set_break(0.2, 0.2)

        pdf.set_table(header, temp, 'LEFT', None)
        pdf.set_page_break()
        return pdf.build()


class ItemOutViewSet(viewsets.ModelViewSet):
    serializer_class = ItemOutSerializer
    queryset = ItemOut.objects.all()

    search_fields = [
        'stockout__numcode',
        'product__name',
    ]

    filterset_fields = [
        'stockout',
        'product',
        'is_init',
    ]
