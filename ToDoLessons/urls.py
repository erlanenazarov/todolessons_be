"""ToDoLessons URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework_simplejwt import views as jwt_views
from rest_framework.routers import DefaultRouter

from ToDoLessons import settings

from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from apps.user import views as user_views
from apps.tasks import views as tasks_views

schema_view = get_schema_view(
    openapi.Info(
        title="TODO Lessons API",
        default_version='v1',
        description="API Documentation",
    ),
    public=True,
)

viewset_router = DefaultRouter()
viewset_router.register('tasks', tasks_views.TaskViewsetAPIView)

attachment_router = DefaultRouter()
attachment_router.register('attachments', tasks_views.TaskAttachmentsViewsetsAPIView)
attachment_router.register('thumbnails', tasks_views.TaskThumbnailViewsetAPIView)


urlpatterns = [
    path('backend/admin/', admin.site.urls),

    path('api/', include([
        path('v1/', include([
            path('auth/', include([
                path('sign-in/', user_views.SignInAPIView.as_view(), name='sign_in'),
                path('sign-up/', user_views.SignUpAPIView.as_view(), name='sign_up'),
                path('refresh-token/', jwt_views.TokenRefreshView.as_view(), name='refresh_token'),
                path('change-password/', user_views.ChangePasswordAPIView.as_view(), name='change_password'),
                path('me/', user_views.ProfileAPIView.as_view(), name='profile'),
            ])),
            path('', include(viewset_router.urls)),
            path('tasks/<uuid:task>/', include(attachment_router.urls)),
        ])),
    ])),

    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui')
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
