from django_filters import rest_framework as filters, DateFilter

from users.models import Customer, Supplier


class CustomerFilter(filters.FilterSet):
    start_date = DateFilter(field_name='created_date', lookup_expr=('gte'), )
    end_date = DateFilter(field_name='created_date', lookup_expr=('lte'))

    class Meta:
        model = Customer
        fields = ['is_init', 'start_date', 'end_date']


class SupplierFilter(filters.FilterSet):
    start_date = DateFilter(field_name='created_date', lookup_expr='gte')
    end_date = DateFilter(field_name='created_date', lookup_expr='lte')

    class Meta:
        model = Supplier
        fields = ['is_init', ]
