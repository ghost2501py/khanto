from rest_framework import serializers

from listings.api_v1.serializers import ListingSerializer

from ..models import Reservation


class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = '__all__'

    def to_representation(self, instance):
        return ReservationReadSerializer().to_representation(instance)

    def validate(self, data):
        if data['check_in'] > data['check_out']:
            raise serializers.ValidationError({
                'check_out': 'Check-out must be after check-in date.',
            })
        return data


class ReservationReadSerializer(serializers.ModelSerializer):

    """Serializer to use when showing/returning a reservation.

    This class displays all `listing` fields instead of just displaying the id.
    It is a separate serializer so it can be integrated with OpenAPI.
    We do not inherit from ReservationSerializer to avoid recursion when using
    `to_representation` method.
    """

    listing = ListingSerializer(read_only=True)

    class Meta:
        model = Reservation
        fields = '__all__'
