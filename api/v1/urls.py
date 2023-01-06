from django.urls import include, path

urlpatterns = [
    path('', include('properties.api_v1.urls')),
    path('', include('listings.api_v1.urls')),
    path('', include('reservations.api_v1.urls')),
]
