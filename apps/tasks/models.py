from django.db import models

from utils.models import AbstractModel
from utils.files import SetUploadPath

# Create your models here.


class Task(AbstractModel):
    class Meta:
        verbose_name = 'Task'
        verbose_name_plural = 'Tasks'
        ordering = ('-created_at',)

    deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)

    done = models.BooleanField(default=False)

    title = models.TextField()
    description = models.TextField(null=True, blank=True)

    user = models.ForeignKey(to='user.User', on_delete=models.CASCADE)


class TaskAttachment(AbstractModel):
    class Meta:
        verbose_name = 'Task Attachment'
        verbose_name_plural = 'Task Attachments'
        ordering = ('-created_at',)

    file = models.FileField(upload_to=SetUploadPath('tasks/attachments'))
    task = models.ForeignKey(to=Task, on_delete=models.CASCADE, related_name='attachments')

    def __str__(self):
        return str(self.file)


class TaskThumbnail(AbstractModel):
    class Meta:
        verbose_name = 'Task Thumbnail'
        verbose_name_plural = 'Task Thumbnails'
        ordering = ('-created_at',)

    file = models.FileField(upload_to=SetUploadPath('tasks/thumbnails'))
    task = models.ForeignKey(to=Task, on_delete=models.CASCADE, related_name='thumbnails')
