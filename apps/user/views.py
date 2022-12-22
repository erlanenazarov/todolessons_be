from rest_framework import generics, exceptions, status
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenViewBase
from drf_yasg.utils import swagger_auto_schema

from django.utils.translation import gettext as _

from apps.user.models import User

from .serializers import (
    LoginSerializer,
    UserCreateSerializer,
    ProfileSerializer,
    ChangePasswordSerializer, UploadAvatarSerializer,
)
from .swagger import TokenResponseSerializer

# Create your views here.


class SignInAPIView(TokenViewBase):
    serializer_class = LoginSerializer

    @swagger_auto_schema(
        operation_summary='Authentication',
        request_body=LoginSerializer(),
        responses={
            200: TokenResponseSerializer()
        }
    )
    def post(self, *args, **kwargs):
        return super(SignInAPIView, self).post(*args, **kwargs)


class SignUpAPIView(generics.CreateAPIView):
    serializer_class = UserCreateSerializer
    response_serializer_class = ProfileSerializer

    @swagger_auto_schema(
        operation_summary='Registration',
        request_body=UserCreateSerializer(),
        responses={
            201: ProfileSerializer(),
        }
    )
    def post(self, *args, **kwargs):
        return super().post(*args, **kwargs)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        profile = self.perform_create(serializer)
        return Response(profile, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        instance = serializer.save()
        response_serializer = self.response_serializer_class(instance=instance)
        return response_serializer.data


class ProfileAPIView(generics.RetrieveAPIView):
    serializer_class = ProfileSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self) -> User:
        return self.request.user

    @swagger_auto_schema(
        operation_summary='Retrieve profile data',
        responses={
            200: ProfileSerializer()
        }
    )
    def get(self, *args, **kwargs):
        return super(ProfileAPIView, self).get(*args, **kwargs)


class UpdateProfileAPIView(generics.UpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user

    @swagger_auto_schema(
        operation_summary='Update account info',
        request_body=ProfileSerializer(),
        responses={
            200: ProfileSerializer()
        }
    )
    def put(self, *args, **kwargs):
        return super().put(*args, **kwargs)

    @swagger_auto_schema(auto_schema=None)
    def patch(self, request, *args, **kwargs):
        raise exceptions.MethodNotAllowed('PATCH')

    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs, partial=True)


class ChangePasswordAPIView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user

    @swagger_auto_schema(
        operation_summary='Change account password',
        request_body=ChangePasswordSerializer(),
        responses={
            200: "{'detail': 'Password successfully updated'}"
        }
    )
    def put(self, *args, **kwargs):
        return super().put(*args, **kwargs)

    @swagger_auto_schema(auto_schema=None)
    def patch(self, request, *args, **kwargs):
        raise exceptions.MethodNotAllowed('PATCH')

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response({'detail': _('Password successfully updated')})

    def perform_update(self, serializer):
        serializer.save()


class UploadUserAvatar(generics.UpdateAPIView):
    serializer_class = UploadAvatarSerializer
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)
    parser_classes = (MultiPartParser,)

    def get_object(self):
        return self.request.user

    @swagger_auto_schema(
        operation_summary='Upload user avatar',
        request_body=UploadAvatarSerializer(),
        responses={
            200: ProfileSerializer()
        }
    )
    def update(self, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=self.request.data, partial=False)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        data = ProfileSerializer(instance=instance).data
        return Response(data)

    @swagger_auto_schema(auto_schema=None)
    def patch(self, *args, **kwargs):
        raise exceptions.MethodNotAllowed('PATCH')
