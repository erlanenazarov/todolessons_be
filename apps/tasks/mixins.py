from rest_framework import exceptions

from django.utils.translation import gettext as _

from apps.tasks.models import Task


class TaskRelatedModelMixin:
    target_attribute = ''

    def get_instance(self) -> Task:
        task_id = self.kwargs.get('task')

        try:
            return Task.objects.get(id=task_id)
        except Task.DoesNotExist:
            raise exceptions.ValidationError({
                'task': [_('Task not found!')]
            })

    def get_queryset(self):
        if not self.target_attribute:
            raise ValueError(_('`.target_attribute` must be set!'))

        task = self.get_instance()
        queryset = getattr(task, self.target_attribute)
        return queryset.all()
