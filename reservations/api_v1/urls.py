from rest_framework import routers

from .views import ReservationViewSet

router = routers.SimpleRouter()
router.register(r'reservations', ReservationViewSet)

urlpatterns = router.urls
