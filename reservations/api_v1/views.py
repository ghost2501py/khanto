from rest_framework import viewsets

from .serializers import ReservationReadSerializer, ReservationSerializer
from ..models import Reservation


class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    http_method_names = ['get', 'post', 'head', 'delete']

    def get_serializer_class(self):
        if hasattr(self, 'action') and self.action in ('list', 'retrieve'):
             return ReservationReadSerializer
        return ReservationSerializer
