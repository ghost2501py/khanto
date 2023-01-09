from rest_framework import serializers

from listings.api_v1.serializers import ListingSerializer

from ..models import Reservation


class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        listing = instance.listing
        representation['listing'] = ListingSerializer().to_representation(listing)
        return representation

    def validate(self, data):
        if data['check_in'] > data['check_out']:
            raise serializers.ValidationError({
                'check_out': 'Check-out must be after check-in date.',
            })
        return data
