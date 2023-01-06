from rest_framework import routers

from .views import ListingViewSet

app_name = 'listings_api_v1'

router = routers.SimpleRouter()
router.register(r'listings', ListingViewSet)

urlpatterns = router.urls
