from rest_framework import viewsets

from .serializers import ReservationSerializer
from ..models import Reservation


class ReservationViewSet(viewsets.ModelViewSet):
    serializer_class = ReservationSerializer
    queryset = Reservation.objects.all()
    http_method_names = ['get', 'post', 'head', 'delete']
