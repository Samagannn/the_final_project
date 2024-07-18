from django_filters import rest_framework as filters
from election.models import Candidate


class ProductFilter(filters.FilterSet):

    from_price = filters.NumberFilter(field_name='price', lookup_expr='gte')
    to_price = filters.NumberFilter(field_name='price', lookup_expr='lte')

    # price = filters.NumericRangeFilter()

    class Meta:
        model = Candidate
        fields = (
            'name',
            'party',
        )