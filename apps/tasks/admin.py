from django.contrib import admin
from .models import Task, TaskThumbnail, TaskAttachment


# Register your models here.


class TaskThumbnailInlineAdmin(admin.TabularInline):
    model = TaskThumbnail
    extra = 1


class TaskAttachmentInlineAdmin(admin.TabularInline):
    model = TaskAttachment
    extra = 1


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'done', 'deleted', 'deleted_at', 'created_at']
    inlines = (TaskThumbnailInlineAdmin, TaskAttachmentInlineAdmin)

