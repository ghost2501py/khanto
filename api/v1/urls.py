from django.urls import include, path

app_name = 'api_v1'

urlpatterns = [
    path('', include('properties.api_v1.urls', namespace='properties')),
    path('', include('listings.api_v1.urls', namespace='listings')),
    path('', include('reservations.api_v1.urls', namespace='reservations')),
]
