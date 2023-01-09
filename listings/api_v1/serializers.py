from rest_framework import serializers

from properties.api_v1.serializers import PropertySerializer

from ..models import Listing


class ListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Listing
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        property = instance.property
        representation['property'] = PropertySerializer().to_representation(property)
        return representation
