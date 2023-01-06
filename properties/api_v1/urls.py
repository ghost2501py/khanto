from rest_framework import routers

from .views import PropertyViewSet

router = routers.SimpleRouter()
router.register(r'properties', PropertyViewSet)

urlpatterns = router.urls
