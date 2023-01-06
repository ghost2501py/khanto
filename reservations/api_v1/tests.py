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
    def setUp(self):
        property = Property.objects.create(
            code='property1',
            guest_limit=5,
            bathrooms=2,
            accept_pets=False,
            cleaning_price=20.0,
        )
        self.listing = Listing.objects.create(
            platform='Airbnb',
            platform_fee='5.00',
            property=property,
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
        self.assertEqual(reservation.check_in, datetime.date(2023, 1, 6))
        self.assertEqual(reservation.check_out, datetime.date(2023, 1, 7))
        self.assertEqual(reservation.price, 50.0)
        self.assertEqual(reservation.total_guests, 2)
        self.assertEqual(reservation.comments, 'Some comment...')
        self.assertEqual(reservation.listing, self.listing)
        self.assertEqual(len(reservation.code), 6)

        self.assertEqual({
            'id': str(reservation.id),
            'check_in': '2023-01-06',
            'check_out': '2023-01-07',
            'price': '50.00',
            'total_guests': 2,
            'comments': 'Some comment...',
            'listing': self.listing.id,
            'code': reservation.code,
            'created_at': reservation.created_at.isoformat().replace('+00:00', 'Z'),
            'updated_at': reservation.updated_at.isoformat().replace('+00:00', 'Z'),
        }, dict(response.data))

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
        Reservation.objects.bulk_create([
            Reservation(
                check_in=datetime.date(2023, 1, 6),
                check_out=datetime.date(2023, 1, 7),
                price=50.0,
                total_guests=1,
                comments='Some comment...',
                listing=self.listing,
                code='CODE1',
            ),
            Reservation(
                check_in=datetime.date(2023, 1, 7),
                check_out=datetime.date(2023, 1, 9),
                price=150.0,
                total_guests=3,
                comments='Some comment...',
                listing=self.listing,
                code='CODE2',
            ),
        ])

        url = reverse('api:v1:reservations:reservation-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

        reservation1 = Reservation.objects.last()
        reservation2 = Reservation.objects.first()

        self.assertEqual(
            [
                {
                    'id': str(reservation2.id),
                    'check_in': '2023-01-07',
                    'check_out': '2023-01-09',
                    'price': '150.00',
                    'total_guests': 3,
                    'comments': 'Some comment...',
                    'listing': str(self.listing.id),
                    'code': 'CODE2',
                    'created_at': reservation2.created_at.isoformat().replace('+00:00', 'Z'),
                    'updated_at': reservation2.updated_at.isoformat().replace('+00:00', 'Z'),
                },
                {
                    'id': str(reservation1.id),
                    'check_in': '2023-01-06',
                    'check_out': '2023-01-07',
                    'price': '50.00',
                    'total_guests': 1,
                    'comments': 'Some comment...',
                    'listing': str(self.listing.id),
                    'code': 'CODE1',
                    'created_at': reservation1.created_at.isoformat().replace('+00:00', 'Z'),
                    'updated_at': reservation1.updated_at.isoformat().replace('+00:00', 'Z'),
                }
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

        self.assertEqual({
            'id': str(reservation.id),
            'check_in': '2023-01-06',
            'check_out': '2023-01-07',
            'price': '50.00',
            'total_guests': 1,
            'comments': 'Some comment...',
            'listing': self.listing.id,
            'code': reservation.code,
            'created_at': reservation.created_at.isoformat().replace('+00:00', 'Z'),
            'updated_at': reservation.updated_at.isoformat().replace('+00:00', 'Z'),
        }, dict(response.data))

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

        reservation.refresh_from_db()
        self.assertEqual(reservation.price, 50.0)

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
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Reservation.objects.count(), 0)
