from collections import OrderedDict

from drf_yasg import openapi
from drf_yasg.inspectors import PaginatorInspector
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class ResultsSetPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'size'
    max_page_size = 100

    def get_paginated_response(self, data):
        return Response({
            'count': self.page.paginator.count,
            'results': data
        })

    def get_paginated_response_schema(self, schema):
        return {
            'type': 'object',
            'properties': {
                'count': {
                    'type': 'integer',
                    'example': 123,
                },
                'results': schema,
            },
        }


class LimitOffsetPaginatorInspectorClass(PaginatorInspector):

    def get_paginated_response(self, paginator, response_schema):
        """
        :param BasePagination paginator: the paginator
        :param openapi.Schema response_schema: the response schema that must be paged.
        :rtype: openapi.Schema
        """

        return openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties=OrderedDict((
                ('count', openapi.Schema(type=openapi.TYPE_INTEGER)),
                ('results', response_schema),
            )),
            required=['results']
        )


SWAGGER_PAGINATION_KWARGS = dict(
    paginator_class=ResultsSetPagination,
    paginator_inspectors=[LimitOffsetPaginatorInspectorClass],
)
