from django.contrib import admin
from django.urls import path, include


api_patterns = [
    path('', include('customer.api.urls')),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include((api_patterns, 'api'), namespace='api'))
]
