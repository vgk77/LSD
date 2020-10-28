from django.contrib import admin
from django.urls import path, include

from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="LSD API",
        default_version='v1',
        description="LSD"
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


api_patterns = [
    path('', include('customer.api.urls')),
    path('', include('telegram.api.urls')),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include((api_patterns, 'api'), namespace='api')),
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui')
]
