from rest_framework import viewsets

from .serializers import ListingReadSerializer, ListingSerializer
from ..models import Listing


class ListingViewSet(viewsets.ModelViewSet):
    queryset = Listing.objects.all()
    http_method_names = ['get', 'post', 'head', 'put', 'patch']

    def get_serializer_class(self):
        if hasattr(self, 'action') and self.action in ('list', 'retrieve'):
             return ListingReadSerializer
        return ListingSerializer
