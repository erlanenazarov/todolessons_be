from drf_yasg.utils import swagger_auto_schema
from rest_framework.parsers import MultiPartParser
from rest_framework import viewsets, exceptions, response
from rest_framework.permissions import IsAuthenticated

from utils.pagination import ResultsSetPagination, SWAGGER_PAGINATION_KWARGS

from .models import Task
from .mixins import TaskRelatedModelMixin
from .filters import TaskFilters
from .serializers import TaskSerializer, TaskThumbnailSerializer, TaskAttachmentSerializer


# Create your views here.

class ViewsetBase(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'put', 'delete', 'options', 'head']
    permission_classes = (IsAuthenticated,)
    pagination_class = ResultsSetPagination

    def update(self, *args, **kwargs):
        return super().update(*args, partial=True, **kwargs)

    @swagger_auto_schema(
        operation_summary='',
        **SWAGGER_PAGINATION_KWARGS,
    )
    def list(self, *args, **kwargs):
        return super().list(*args, **kwargs)


class TaskViewsetAPIView(ViewsetBase):
    serializer_class = TaskSerializer
    queryset = Task.objects.all()
    filterset_class = TaskFilters

    def get_queryset(self):
        return self.queryset.filter(user_id=self.request.user.id)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({
            'user': self.request.user
        })
        return context


class TaskAttachmentsViewsetsAPIView(TaskRelatedModelMixin, ViewsetBase):
    serializer_class = TaskAttachmentSerializer
    queryset = TaskAttachmentSerializer.Meta.model.objects.all()
    target_attribute = 'attachments'
    parser_classes = [MultiPartParser]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({'task': self.get_instance()})
        return context


class TaskThumbnailViewsetAPIView(TaskRelatedModelMixin, ViewsetBase):
    serializer_class = TaskThumbnailSerializer
    queryset = TaskThumbnailSerializer.Meta.model.objects.all()
    target_attribute = 'thumbnails'
    parser_classes = [MultiPartParser]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({'task': self.get_instance()})
        return context
