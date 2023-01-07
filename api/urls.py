from rest_framework.schemas import get_schema_view

from django.urls import include, path
from django.views.generic import TemplateView

app_name = 'api'

schema_url_patterns_v1 = [
    path('api/v1/', include('api.v1.urls', namespace='v1')),
]

schema_view = get_schema_view(
    title='Khanto API',
    description='Khanto API',
    version='1.0.0',
    patterns=schema_url_patterns_v1,
)

urlpatterns = [
    path('api/v1/openapi/', schema_view, name='openapi-schema-v1'),
    path('api/v1/docs/', TemplateView.as_view(
        template_name='swagger-ui.html',
        extra_context={'schema_url': 'api:openapi-schema-v1'}
    ), name='swagger-ui'),
]
urlpatterns += schema_url_patterns_v1
