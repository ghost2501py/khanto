from django.urls import include, path

urlpatterns = [
    path('', include('properties.api_v1.urls')),
]
