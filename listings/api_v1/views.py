from rest_framework import viewsets

from .serializers import ListingSerializer
from ..models import Listing


class ListingViewSet(viewsets.ModelViewSet):
    serializer_class = ListingSerializer
    queryset = Listing.objects.all()
    http_method_names = ['get', 'post', 'head', 'put', 'patch']
