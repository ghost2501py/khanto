import json
import datetime

from rest_framework import status
from rest_framework.test import APITestCase

from django.urls import reverse

from ..models import Property


class PropertyTests(APITestCase):
    maxDiff = None

    def test_create_property(self):
        """
        Ensure we can create a new property object.
        """
        self.assertEqual(Property.objects.count(), 0)

        data = {
            'code': 'property1',
            'guest_limit': 5,
            'bathrooms': 2,
            'accept_pets': False,
            'cleaning_price': '20.00',
            'activation_date': '2023-01-06',
        }
        url = reverse('api:v1:properties:property-list')
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Property.objects.count(), 1)

        property = Property.objects.get()
        self.assertDictEqual({
            'id': str(property.id),
            'code': data['code'],
            'guest_limit': data['guest_limit'],
            'bathrooms': data['bathrooms'],
            'accept_pets': data['accept_pets'],
            'cleaning_price': data['cleaning_price'],
            'activation_date': data['activation_date'],
            'created_at': property.created_at.isoformat().replace('+00:00', 'Z'),
            'updated_at': property.updated_at.isoformat().replace('+00:00', 'Z'),
        }, dict(response.data))

    def test_list_property(self):
        """
        Ensure we can list properties.
        """
        property1 = Property.objects.create(
            code='property1',
            guest_limit=5,
            bathrooms=2,
            accept_pets=False,
            cleaning_price=20.0,
        )
        property2 = Property.objects.create(
            code='property2',
            guest_limit=3,
            bathrooms=1,
            accept_pets=True,
            cleaning_price=10.0,
            activation_date=datetime.date(2023, 1, 6),
        )

        url = reverse('api:v1:properties:property-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

        self.assertEqual(
            [
                {
                    'id': str(property2.id),
                    'code': property2.code,
                    'guest_limit': property2.guest_limit,
                    'bathrooms': property2.bathrooms,
                    'accept_pets': property2.accept_pets,
                    'cleaning_price': '{:.2f}'.format(property2.cleaning_price),
                    'activation_date': property2.activation_date.isoformat().replace('+00:00', 'Z'),
                    'created_at': property2.created_at.isoformat().replace('+00:00', 'Z'),
                    'updated_at': property2.updated_at.isoformat().replace('+00:00', 'Z'),
                },
                {
                    'id': str(property1.id),
                    'code': property1.code,
                    'guest_limit': property1.guest_limit,
                    'bathrooms': property1.bathrooms,
                    'accept_pets': property1.accept_pets,
                    'cleaning_price': '{:.2f}'.format(property1.cleaning_price),
                    'activation_date': property1.activation_date,
                    'created_at': property1.created_at.isoformat().replace('+00:00', 'Z'),
                    'updated_at': property1.updated_at.isoformat().replace('+00:00', 'Z'),
                },

            ],
            json.loads(json.dumps(response.data)),
        )

    def test_retrieve_property(self):
        """
        Ensure we can retrieve a property by id.
        """
        property = Property.objects.create(
            code='property1',
            guest_limit=5,
            bathrooms=2,
            accept_pets=False,
            cleaning_price=20.0,
            activation_date=datetime.date(2023, 1, 6),
        )

        url = reverse('api:v1:properties:property-detail', kwargs={'pk': property.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertDictEqual({
            'id': str(property.id),
            'code': property.code,
            'guest_limit': property.guest_limit,
            'bathrooms': property.bathrooms,
            'accept_pets': property.accept_pets,
            'cleaning_price': '{:.2f}'.format(property.cleaning_price),
            'activation_date': property.activation_date.isoformat().replace('+00:00', 'Z'),
            'created_at': property.created_at.isoformat().replace('+00:00', 'Z'),
            'updated_at': property.updated_at.isoformat().replace('+00:00', 'Z'),
        }, dict(response.data))

    def test_update_property(self):
        """
        Ensure we can update a property.
        """
        property = Property.objects.create(
            code='property1',
            guest_limit=5,
            bathrooms=2,
            accept_pets=False,
            cleaning_price=20.0,
        )

        data = {
            'code': 'property2',
            'guest_limit': 3,
            'bathrooms': 1,
            'accept_pets': True,
            'cleaning_price': '10.00',
            'activation_date': '2023-01-07',
        }
        url = reverse('api:v1:properties:property-detail', kwargs={'pk': property.id})
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        property.refresh_from_db()
        self.assertDictEqual({
            'id': str(property.id),
            'code': data['code'],
            'guest_limit': data['guest_limit'],
            'bathrooms': data['bathrooms'],
            'accept_pets': data['accept_pets'],
            'cleaning_price': data['cleaning_price'],
            'activation_date': data['activation_date'],
            'created_at': property.created_at.isoformat().replace('+00:00', 'Z'),
            'updated_at': property.updated_at.isoformat().replace('+00:00', 'Z'),
        }, dict(response.data))

    def test_delete_property(self):
        """
        Ensure we can delete a property.
        """
        property = Property.objects.create(
            code='property1',
            guest_limit=5,
            bathrooms=2,
            accept_pets=False,
            cleaning_price=20.0,
        )
        self.assertEqual(Property.objects.count(), 1)
        url = reverse('api:v1:properties:property-detail', kwargs={'pk': property.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Property.objects.count(), 0)
