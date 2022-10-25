from django_filters import filters
from django_filters.rest_framework import filterset

from .models import Task

SORT_CHOICES = (
    ('created_at', 'created_at ASC'),
    ('-created_at', 'created_at DESC')
)


class TaskFilters(filterset.FilterSet):
    sort = filters.OrderingFilter(fields=(
        ('created_at', 'Created at'),
        ('updated_at', 'Updated at')
    ))
    title = filters.CharFilter(field_name='title', lookup_expr='icontains')
    start_date = filters.DateTimeFilter(field_name='created_at', lookup_expr='gte')
    finish_date = filters.DateTimeFilter(field_name='created_at', lookup_expr='lte')

    class Meta:
        model = Task
        fields = {
            'done': ['exact']
        }
