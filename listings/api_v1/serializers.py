from rest_framework import serializers

from properties.api_v1.serializers import PropertySerializer

from ..models import Listing


class ListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Listing
        fields = '__all__'

    def to_representation(self, instance):
        return ListingReadSerializer().to_representation(instance)


class ListingReadSerializer(serializers.ModelSerializer):

    """Serializer to use when showing/returning a listing.

    This class returns all `property` fields instead of just returning the id.
    It is a separate serializer so it can be integrated with OpenAPI.
    We do not inherit from ListingSerializer to avoid recursion when using
    `to_representation` method.
    """

    property = PropertySerializer(read_only=True)

    class Meta:
        model = Listing
        fields = '__all__'
