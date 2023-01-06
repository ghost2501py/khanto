from rest_framework import routers

from .views import ReservationViewSet

app_name = 'reservations_api_v1'

router = routers.SimpleRouter()
router.register(r'reservations', ReservationViewSet)

urlpatterns = router.urls
