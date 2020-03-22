from django_filters import rest_framework as filters, DateFilter

from stocks.models import StockIn


class StockInFilter(filters.FilterSet):
    start_date = DateFilter(field_name='date', lookup_expr='gte')
    end_date = DateFilter(field_name='date', lookup_expr='lte')

    class Meta:
        model = StockIn
        fields = ['is_init', 'numcode', 'user', 'supplier']
