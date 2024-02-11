from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from .models import MyUser

class UserViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_data = {
            'username': 'testuser',
            'password': 'password123'
        }
        self.user = MyUser.objects.create_user(**self.user_data)

    def test_user_registration(self):
        url = reverse('users:register')
        data = {
            'username': 'admin',
            'password': 'admin123',
            'password2': 'admin123',  # Ensure this matches the 'password' field
        }
        response = self.client.post(url, data, format='json')
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_login(self):
        response = self.client.post(reverse('users:login'), {
            'username': self.user_data['username'],
            'password': self.user_data['password'],
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('msg' in response.data)
        self.assertEqual(response.data['msg'], 'Login Success')

    def test_user_logout(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(reverse('users:logout'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_change_password(self):
        self.client.force_authenticate(user=self.user)  # Make sure self.user is the user you're testing with
        # Set a known password for the user, if not already set
        self.user.set_password('oldpassword')
        self.user.save()
        url = reverse('users:change-password')
        data = {
            'current_password': 'oldpassword',
            'new_password': 'newpassword123',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)