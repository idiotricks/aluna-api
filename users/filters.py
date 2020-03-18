from django_filters import rest_framework as filters, DateFilter

from users.models import Customer


class CustomerFilter(filters.FilterSet):
    start_date = DateFilter(field_name='created_date', lookup_expr=('lt'), )
    end_date = DateFilter(field_name='created_date', lookup_expr=('gt'))

    class Meta:
        model = Customer
        fields = ['is_init', 'start_date', 'end_date']
