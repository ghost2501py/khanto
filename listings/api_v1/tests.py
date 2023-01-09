import json

from rest_framework import status
from rest_framework.test import APITestCase

from django.core.serializers.json import DjangoJSONEncoder
from django.urls import reverse

from properties.models import Property

from ..models import Listing


class ListingTests(APITestCase):
    maxDiff = None

    def setUp(self):
        self.property = Property.objects.create(
            code='property1',
            guest_limit=5,
            bathrooms=2,
            accept_pets=False,
            cleaning_price=20.0,
        )

    def test_create_listing(self):
        """
        Ensure we can create a new listing object.
        """
        self.assertEqual(Listing.objects.count(), 0)

        data = {
            'platform': 'Airbnb',
            'platform_fee': '5.00',
            'property': self.property.id,
        }
        url = reverse('api:v1:listings:listing-list')
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Listing.objects.count(), 1)

        listing = Listing.objects.get()
        self.assertDictEqual({
            'id': str(listing.id),
            'platform': data['platform'],
            'platform_fee': data['platform_fee'],
            'created_at': listing.created_at.isoformat().replace('+00:00', 'Z'),
            'updated_at': listing.updated_at.isoformat().replace('+00:00', 'Z'),
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
        }, json.loads(json.dumps(response.data, cls=DjangoJSONEncoder)))

    def test_list_listing(self):
        """
        Ensure we can list listings.
        """
        listing1 = Listing.objects.create(
            platform='Airbnb',
            platform_fee=5.0,
            property=self.property,
        )
        listing2 = Listing.objects.create(
            platform='Cloudbeds',
            platform_fee=4.0,
            property=self.property,
        )

        url = reverse('api:v1:listings:listing-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

        self.assertEqual(
            [
                {
                    'id': str(listing2.id),
                    'platform': listing2.platform,
                    'platform_fee': '{:.2f}'.format(listing2.platform_fee),
                    'created_at': listing2.created_at.isoformat().replace('+00:00', 'Z'),
                    'updated_at': listing2.updated_at.isoformat().replace('+00:00', 'Z'),
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
                {
                    'id': str(listing1.id),
                    'platform': listing1.platform,
                    'platform_fee': '{:.2f}'.format(listing1.platform_fee),
                    'created_at': listing1.created_at.isoformat().replace('+00:00', 'Z'),
                    'updated_at': listing1.updated_at.isoformat().replace('+00:00', 'Z'),
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
                }
            ],
            json.loads(json.dumps(response.data, cls=DjangoJSONEncoder)),
        )

    def test_retrieve_listing(self):
        """
        Ensure we can retrieve a listing by id.
        """
        listing = Listing.objects.create(
            platform='Airbnb',
            platform_fee=5.0,
            property=self.property,
        )

        url = reverse('api:v1:listings:listing-detail', kwargs={'pk': listing.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertDictEqual({
            'id': str(listing.id),
            'platform': listing.platform,
            'platform_fee': '{:.2f}'.format(listing.platform_fee),
            'created_at': listing.created_at.isoformat().replace('+00:00', 'Z'),
            'updated_at': listing.updated_at.isoformat().replace('+00:00', 'Z'),
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
        }, json.loads(json.dumps(response.data, cls=DjangoJSONEncoder)))

    def test_update_listing(self):
        """
        Ensure we can update a listing.
        """
        listing = Listing.objects.create(
            platform='Cloudbeds',
            platform_fee=4.0,
            property=self.property,
        )

        property2 = Property.objects.create(
            code='property2',
            guest_limit=5,
            bathrooms=2,
            accept_pets=False,
            cleaning_price=20.0,
        )

        data = {
            'platform': 'Airbnb',
            'platform_fee': '5.00',
            'property': property2.id,
        }
        url = reverse('api:v1:listings:listing-detail', kwargs={'pk': listing.id})
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        listing.refresh_from_db()
        self.assertDictEqual({
            'id': str(listing.id),
            'platform': data['platform'],
            'platform_fee': data['platform_fee'],
            'created_at': listing.created_at.isoformat().replace('+00:00', 'Z'),
            'updated_at': listing.updated_at.isoformat().replace('+00:00', 'Z'),
            'property': {
                'id': str(property2.id),
                'code': property2.code,
                'guest_limit': property2.guest_limit,
                'bathrooms': property2.bathrooms,
                'accept_pets': property2.accept_pets,
                'cleaning_price': '{:.2f}'.format(property2.cleaning_price),
                'activation_date': property2.activation_date,
                'created_at': property2.created_at.isoformat().replace('+00:00', 'Z'),
                'updated_at': property2.updated_at.isoformat().replace('+00:00', 'Z'),
            },
        }, json.loads(json.dumps(response.data, cls=DjangoJSONEncoder)))

    def test_delete_listing(self):
        """
        Ensure we can't delete a listing.
        """
        listing = Listing.objects.create(
            platform='Cloudbeds',
            platform_fee=4.0,
            property=self.property,
        )
        self.assertEqual(Listing.objects.count(), 1)
        url = reverse('api:v1:listings:listing-detail', kwargs={'pk': listing.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(Listing.objects.count(), 1)
