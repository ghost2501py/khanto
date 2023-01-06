from rest_framework import routers

from .views import PropertyViewSet

app_name = 'properties_v1'

router = routers.SimpleRouter()
router.register(r'properties', PropertyViewSet)

urlpatterns = router.urls
