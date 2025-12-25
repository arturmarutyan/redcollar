from django_filters import rest_framework as filters
from .models import Message


class MessageFilter(filters.FilterSet):
    point = filters.NumberFilter(field_name='point__id')
    author = filters.CharFilter(field_name='author', lookup_expr='icontains')
    
    class Meta:
        model = Message
        fields = ['point', 'author']