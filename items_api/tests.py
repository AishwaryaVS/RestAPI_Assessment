from django.test import TestCase

# Create your tests here.
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Items
from .serializers import ItemSerializer

class ItemsTests(APITestCase):
    def setUp(self):
        self._modify_permissions_for_testing()
        # Create some items for testing
        Items.objects.create(sku='SKU001', name='Item 1', category='Category 1', in_stock=True, quantity=10)
        Items.objects.create(sku='SKU002', name='Item 2', category='Category 2', in_stock=False, quantity=5)

    def _modify_permissions_for_testing(self):
        from rest_framework import permissions
        from .views import ItemsListApiView
        
        ItemsListApiView.permission_classes = [permissions.AllowAny]  # Allow unauthenticated access for testing

    def test_get_items_list(self):
         # Test to verify GET endpoint API calls.
        url = reverse('items-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_create_item(self):
        # Test to verify POST endpoint API calls.
        url = reverse('items-list')
        initial_item_count = Items.objects.count()
        data = {
            'sku': 'SKU00TEST',
            'name': 'Test Item',
            'category': 'Test Category',
            'tags': 'Test Tags',
            'in_stock': True,
            'quantity': 15
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Check if total count of items has increased by 1
        self.assertEqual(Items.objects.count(), initial_item_count + 1)

        # Check if item is created correctly in the database
        created_item = Items.objects.filter(sku='SKU00TEST').first()
        self.assertIsNotNone(created_item)
        self.assertEqual(created_item.name, 'Test Item')
        self.assertEqual(created_item.category, 'Test Category')
        self.assertEqual(created_item.tags, 'Test Tags')
        self.assertTrue(created_item.in_stock)
        self.assertEqual(created_item.quantity, 15)

    def test_invalid_create_item(self):
        # Test case to ensure we cannot create an item with invalid data
        url = reverse('items-list')
        data = {
            'sku': 'SKU004',
            'name': 'Item 4',
            # Missing required 'category' field
            'in_stock': True,
            'quantity': 20
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
