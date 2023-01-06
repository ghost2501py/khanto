import json

from rest_framework import status
from rest_framework.test import APITestCase

from django.core.serializers.json import DjangoJSONEncoder
from django.urls import reverse

from properties.models import Property

from ..models import Listing


class ListingTests(APITestCase):
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
        self.assertEqual(listing.platform, 'Airbnb')
        self.assertEqual(listing.platform_fee, 5.0)

        self.assertEqual({
            'id': str(listing.id),
            'platform': 'Airbnb',
            'platform_fee': '5.00',
            'property': self.property.id,
            'created_at': listing.created_at.isoformat().replace('+00:00', 'Z'),
            'updated_at': listing.updated_at.isoformat().replace('+00:00', 'Z'),
        }, dict(response.data))

    def test_list_listing(self):
        """
        Ensure we can list listings.
        """
        Listing.objects.bulk_create([
            Listing(
                platform='Airbnb',
                platform_fee='5.00',
                property=self.property,
            ),
            Listing(
                platform='Cloudbeds',
                platform_fee='4.00',
                property=self.property,
            ),
        ])

        url = reverse('api:v1:listings:listing-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

        listing1 = Listing.objects.last()
        listing2 = Listing.objects.first()
        self.assertEqual(
            [
                {
                    'id': str(listing2.id),
                    'platform': 'Cloudbeds',
                    'platform_fee': '4.00',
                    'property': str(self.property.id),
                    'created_at': listing2.created_at.isoformat().replace('+00:00', 'Z'),
                    'updated_at': listing2.updated_at.isoformat().replace('+00:00', 'Z'),
                },
                {
                    'id': str(listing1.id),
                    'platform': 'Airbnb',
                    'platform_fee': '5.00',
                    'property': str(self.property.id),
                    'created_at': listing1.created_at.isoformat().replace('+00:00', 'Z'),
                    'updated_at': listing1.updated_at.isoformat().replace('+00:00', 'Z'),
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
            platform_fee='5.00',
            property=self.property,
        )

        url = reverse('api:v1:listings:listing-detail', kwargs={'pk': listing.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual({
            'id': str(listing.id),
            'platform': 'Airbnb',
            'platform_fee': '5.00',
            'property': self.property.id,
            'created_at': listing.created_at.isoformat().replace('+00:00', 'Z'),
            'updated_at': listing.updated_at.isoformat().replace('+00:00', 'Z'),
        }, dict(response.data))

    def test_update_listing(self):
        """
        Ensure we can update a listing.
        """
        listing = Listing.objects.create(
            platform='Cloudbeds',
            platform_fee='4.00',
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
        self.assertEqual(listing.platform, 'Airbnb')
        self.assertEqual(listing.platform_fee, 5.0)
        self.assertEqual(listing.property, property2)

    def test_delete_listing(self):
        """
        Ensure we can't delete a listing.
        """
        listing = Listing.objects.create(
            platform='Cloudbeds',
            platform_fee='4.00',
            property=self.property,
        )

        self.assertEqual(Listing.objects.count(), 1)
        url = reverse('api:v1:listings:listing-detail', kwargs={'pk': listing.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(Listing.objects.count(), 1)
