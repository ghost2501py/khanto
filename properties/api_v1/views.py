from rest_framework import viewsets

from .serializers import PropertySerializer
from ..models import Property


class PropertyViewSet(viewsets.ModelViewSet):
    serializer_class = PropertySerializer
    queryset = Property.objects.all()
