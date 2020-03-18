from django_filters import rest_framework as filters, DateFilter

from products.models import Product


class ProductFilter(filters.FilterSet):
    start_date = DateFilter(field_name='created_date', lookup_expr='gte')
    end_date = DateFilter(field_name='created_date', lookup_expr='lte')

    class Meta:
        model = Product
        fields = [
            'numcode',
            'user',
            'is_init',
        ]
