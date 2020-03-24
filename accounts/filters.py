import django_filters
from django_filters import DateFilter, CharFilter
from .models import Order


class OrderFilter(django_filters.FilterSet):
    startDate = DateFilter(field_name='dateCreated', lookup_expr='gte')
    #lookup_expr sadece bir yazi eklemek icin mi yoksa filtering yapiyor mu
    endDate = DateFilter(field_name='dateCreated', lookup_expr='lte')
    note = CharFilter(field_name='note')

    class Meta:
        model = Order
        fields = ('product','status')

