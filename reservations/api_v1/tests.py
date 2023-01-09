import json
import datetime

from rest_framework import status
from rest_framework.test import APITestCase

from django.core.serializers.json import DjangoJSONEncoder
from django.urls import reverse

from listings.models import Listing
from properties.models import Property

from ..models import Reservation


class ReservationTests(APITestCase):
    maxDiff = None

    def setUp(self):
        self.property = Property.objects.create(
            code='property1',
            guest_limit=5,
            bathrooms=2,
            accept_pets=False,
            cleaning_price=20.0,
        )
        self.listing = Listing.objects.create(
            platform='Airbnb',
            platform_fee=5.00,
            property=self.property,
        )

    def test_create_reservation(self):
        """
        Ensure we can create a new reservation object.
        """
        self.assertEqual(Reservation.objects.count(), 0)

        data = {
            'check_in': '2023-01-06',
            'check_out': '2023-01-07',
            'price': '50.00',
            'total_guests': 2,
            'comments': 'Some comment...',
            'listing': self.listing.id,
        }
        url = reverse('api:v1:reservations:reservation-list')
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Reservation.objects.count(), 1)

        reservation = Reservation.objects.get()
        self.assertDictEqual({
            'id': str(reservation.id),
            'check_in': data['check_in'],
            'check_out': data['check_out'],
            'price': data['price'],
            'total_guests': data['total_guests'],
            'comments': data['comments'],
            'code': reservation.code,
            'created_at': reservation.created_at.isoformat().replace('+00:00', 'Z'),
            'updated_at': reservation.updated_at.isoformat().replace('+00:00', 'Z'),
            'listing': {
                'id': str(self.listing.id),
                'platform': self.listing.platform,
                'platform_fee': '{:.2f}'.format(self.listing.platform_fee),
                'created_at': self.listing.created_at.isoformat().replace('+00:00', 'Z'),
                'updated_at': self.listing.updated_at.isoformat().replace('+00:00', 'Z'),
                'property': {
                    'id': str(self.property.id),
                    'code': self.property.code,
                    'guest_limit': self.property.guest_limit,
                    'bathrooms': self.property.bathrooms,
                    'accept_pets': self.property.accept_pets,
                    'cleaning_price': '{:.2f}'.format(self.property.cleaning_price),
                    'activation_date': self.property.activation_date,
                    'created_at': self.property.created_at.isoformat().replace('+00:00', 'Z'),
                    'updated_at': self.property.updated_at.isoformat().replace('+00:00', 'Z'),
                },
            },
        }, json.loads(json.dumps(response.data)))

    def test_create_reservation_with_invalid_check_out(self):
        """
        Ensure we can't create a reservation if check_in is after check_out.
        """
        self.assertEqual(Reservation.objects.count(), 0)

        data = {
            'check_in': '2023-01-06',
            'check_out': '2023-01-05',
            'price': '50.00',
            'total_guests': 2,
            'comments': 'Some comment...',
            'listing': self.listing.id,
        }
        url = reverse('api:v1:reservations:reservation-list')
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Reservation.objects.count(), 0)
        self.assertEqual({
            'check_out': ['Check-out must be after check-in date.'],
        }, json.loads(json.dumps(response.data)))

    def test_list_reservations(self):
        """
        Ensure we can list reservations.
        """
        reservation1 = Reservation.objects.create(
            check_in=datetime.date(2023, 1, 6),
            check_out=datetime.date(2023, 1, 7),
            price=50.0,
            total_guests=1,
            comments='Some comment...',
            listing=self.listing,
        )
        reservation2 = Reservation.objects.create(
            check_in=datetime.date(2023, 1, 7),
            check_out=datetime.date(2023, 1, 9),
            price=150.0,
            total_guests=3,
            comments='Some comment...',
            listing=self.listing,
        )

        url = reverse('api:v1:reservations:reservation-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

        self.assertEqual(
            [
                {
                    'id': str(reservation2.id),
                    'check_in': reservation2.check_in.isoformat().replace('+00:00', 'Z'),
                    'check_out': reservation2.check_out.isoformat().replace('+00:00', 'Z'),
                    'price': '{:.2f}'.format(reservation2.price),
                    'total_guests': reservation2.total_guests,
                    'comments': reservation2.comments,
                    'code': reservation2.code,
                    'created_at': reservation2.created_at.isoformat().replace('+00:00', 'Z'),
                    'updated_at': reservation2.updated_at.isoformat().replace('+00:00', 'Z'),
                    'listing': {
                        'id': str(self.listing.id),
                        'platform': self.listing.platform,
                        'platform_fee': '{:.2f}'.format(self.listing.platform_fee),
                        'created_at': self.listing.created_at.isoformat().replace('+00:00', 'Z'),
                        'updated_at': self.listing.updated_at.isoformat().replace('+00:00', 'Z'),
                        'property': {
                            'id': str(self.property.id),
                            'code': self.property.code,
                            'guest_limit': self.property.guest_limit,
                            'bathrooms': self.property.bathrooms,
                            'accept_pets': self.property.accept_pets,
                            'cleaning_price': '{:.2f}'.format(self.property.cleaning_price),
                            'activation_date': self.property.activation_date,
                            'created_at': self.property.created_at.isoformat().replace('+00:00', 'Z'),
                            'updated_at': self.property.updated_at.isoformat().replace('+00:00', 'Z'),
                        },
                    },
                },
                {
                    'id': str(reservation1.id),
                    'check_in': reservation1.check_in.isoformat().replace('+00:00', 'Z'),
                    'check_out': reservation1.check_out.isoformat().replace('+00:00', 'Z'),
                    'price': '{:.2f}'.format(reservation1.price),
                    'total_guests': reservation1.total_guests,
                    'comments': reservation1.comments,
                    'code': reservation1.code,
                    'created_at': reservation1.created_at.isoformat().replace('+00:00', 'Z'),
                    'updated_at': reservation1.updated_at.isoformat().replace('+00:00', 'Z'),
                    'listing': {
                        'id': str(self.listing.id),
                        'platform': self.listing.platform,
                        'platform_fee': '{:.2f}'.format(self.listing.platform_fee),
                        'created_at': self.listing.created_at.isoformat().replace('+00:00', 'Z'),
                        'updated_at': self.listing.updated_at.isoformat().replace('+00:00', 'Z'),
                        'property': {
                            'id': str(self.property.id),
                            'code': self.property.code,
                            'guest_limit': self.property.guest_limit,
                            'bathrooms': self.property.bathrooms,
                            'accept_pets': self.property.accept_pets,
                            'cleaning_price': '{:.2f}'.format(self.property.cleaning_price),
                            'activation_date': self.property.activation_date,
                            'created_at': self.property.created_at.isoformat().replace('+00:00', 'Z'),
                            'updated_at': self.property.updated_at.isoformat().replace('+00:00', 'Z'),
                        },
                    },
                },
            ],
            json.loads(json.dumps(response.data, cls=DjangoJSONEncoder)),
        )

    def test_retrieve_reservation(self):
        """
        Ensure we can retrieve a reservation by id.
        """
        reservation = Reservation.objects.create(
            check_in=datetime.date(2023, 1, 6),
            check_out=datetime.date(2023, 1, 7),
            price=50.0,
            total_guests=1,
            comments='Some comment...',
            listing=self.listing,
        )

        url = reverse('api:v1:reservations:reservation-detail', kwargs={'pk': reservation.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertDictEqual({
            'id': str(reservation.id),
            'check_in': reservation.check_in.isoformat().replace('+00:00', 'Z'),
            'check_out': reservation.check_out.isoformat().replace('+00:00', 'Z'),
            'price': '{:.2f}'.format(reservation.price),
            'total_guests': reservation.total_guests,
            'comments': reservation.comments,
            'code': reservation.code,
            'created_at': reservation.created_at.isoformat().replace('+00:00', 'Z'),
            'updated_at': reservation.updated_at.isoformat().replace('+00:00', 'Z'),
            'listing': {
                'id': str(self.listing.id),
                'platform': self.listing.platform,
                'platform_fee': '{:.2f}'.format(self.listing.platform_fee),
                'created_at': self.listing.created_at.isoformat().replace('+00:00', 'Z'),
                'updated_at': self.listing.updated_at.isoformat().replace('+00:00', 'Z'),
                'property': {
                    'id': str(self.property.id),
                    'code': self.property.code,
                    'guest_limit': self.property.guest_limit,
                    'bathrooms': self.property.bathrooms,
                    'accept_pets': self.property.accept_pets,
                    'cleaning_price': '{:.2f}'.format(self.property.cleaning_price),
                    'activation_date': self.property.activation_date,
                    'created_at': self.property.created_at.isoformat().replace('+00:00', 'Z'),
                    'updated_at': self.property.updated_at.isoformat().replace('+00:00', 'Z'),
                },
            },
        }, json.loads(json.dumps(response.data)))

    def test_update_reservation(self):
        """
        Ensure we can't update a reservation.
        """
        reservation = Reservation.objects.create(
            check_in=datetime.date(2023, 1, 6),
            check_out=datetime.date(2023, 1, 7),
            price=50.0,
            total_guests=1,
            comments='Some comment...',
            listing=self.listing,
        )
        url = reverse('api:v1:reservations:reservation-detail', kwargs={'pk': reservation.id})
        response = self.client.put(url, {'price': 100.0})
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_delete_reservation(self):
        """
        Ensure we can delete a reservation.
        """
        reservation = Reservation.objects.create(
            check_in=datetime.date(2023, 1, 6),
            check_out=datetime.date(2023, 1, 7),
            price=50.0,
            total_guests=1,
            comments='Some comment...',
            listing=self.listing,
        )
        url = reverse('api:v1:reservations:reservation-detail', kwargs={'pk': reservation.id})
        self.assertEqual(Reservation.objects.count(), 1)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Reservation.objects.count(), 0)
