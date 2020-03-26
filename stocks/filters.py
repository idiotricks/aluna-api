from django_filters import rest_framework as filters, DateFilter

from stocks.models import StockIn, StockOut, StockCard


class StockCardFilter(filters.FilterSet):
    start_date = DateFilter(field_name='date', lookup_expr='gte')
    end_date = DateFilter(field_name='date', lookup_expr='lte')

    class Meta:
        model = StockCard
        fields = [
            'numcode',
            'product',
            'is_init',
        ]


class StockInFilter(filters.FilterSet):
    start_date = DateFilter(field_name='date', lookup_expr='gte')
    end_date = DateFilter(field_name='date', lookup_expr='lte')

    class Meta:
        model = StockIn
        fields = ['is_init', 'numcode', 'user', 'supplier']


class StockOutFilter(filters.FilterSet):
    start_date = DateFilter(field_name='date', lookup_expr='gte')
    end_date = DateFilter(field_name='date', lookup_expr='lte')

    class Meta:
        model = StockOut
        fields = ['is_init', 'numcode', 'user', 'customer']
