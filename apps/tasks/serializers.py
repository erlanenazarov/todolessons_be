from rest_framework import serializers

from .models import Task, TaskThumbnail, TaskAttachment


class TaskThumbnailSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskThumbnail
        fields = (
            'id',
            'file',
            'created_at',
            'updated_at',
        )
        extra_args = {
            'id': {
                'read_only': True
            },
            'created_at': {
                'read_only': True,
            },
            'updated_at': {
                'read_only': True,
            },
        }

    def create(self, validated_data):
        task = self.context.get('task')
        validated_data.update({'task_id': task.id})
        return super().create(validated_data)


class TaskAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskAttachment
        fields = (
            'id',
            'file',
            'created_at',
            'updated_at',
        )
        extra_args = {
            'id': {
                'read_only': True
            },
            'created_at': {
                'read_only': True,
            },
            'updated_at': {
                'read_only': True,
            },
        }

    def create(self, validated_data):
        task = self.context.get('task')
        validated_data.update({'task_id': task.id})
        return super().create(validated_data)


class TaskSerializer(serializers.ModelSerializer):
    attachments = TaskAttachmentSerializer(many=True, read_only=True)
    thumbnails = TaskThumbnailSerializer(many=True, read_only=True)

    class Meta:
        model = Task
        fields = (
            'id',
            'title',
            'description',
            'done',
            'deleted',
            'deleted_at',
            'created_at',
            'updated_at',
            'attachments',
            'thumbnails',
            'user',
        )

    def create(self, validated_data):
        user = self.context.get('user')
        validated_data.update({'user_id': user.id})
        return super().create(validated_data)


class UploadFileSerializer(serializers.Serializer):
    file = serializers.FileField()

    def create(self, validated_data):
        raise NotImplementedError('UploadFileSerializer cannot create an instance')

    def update(self, instance, validated_data):
        raise NotImplementedError('UploadFileSerializer cannot update anything')
