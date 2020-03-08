import json

from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from helpers.models import auto_number
from users.models import Customer


class UsersTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='test', password='test')
        self.token = Token.objects.get(user=self.user)

    def api_auth(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token}')

    def test_user_create_authenticated(self):
        self.api_auth()
        response = self.client.post('/users/')
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_user_put_authenticated(self):
        self.api_auth()
        response = self.client.put('/users/')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_user_patch_authenticated(self):
        self.api_auth()
        response = self.client.patch('/users/')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_user_delete_authenticated(self):
        self.api_auth()
        response = self.client.delete('/users/')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_user_list_authenticated(self):
        self.api_auth()
        response = self.client.get('/users/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_get_authenticated(self):
        self.api_auth()
        response = self.client.get(f'/users/{self.user.pk}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_get_un_authenticated(self):
        response = self.client.get(f'/users/{self.user.pk}/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_create_un_authenticated(self):
        response = self.client.post('/users/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_patch_un_authenticated(self):
        response = self.client.post('/users/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_list_un_authenticated(self):
        response = self.client.get('/users/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_customer_create_authenticated(self):
        self.api_auth()
        code_number = auto_number(Customer, 'CSR')
        payload = {
            'code_number': code_number,
            'name': 'Adelia',
            'phone': '+628900987',
            'address': '42 Street',
        }

        response = self.client.post('/customers/', payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_customer_create_un_authenticated(self):
        payload = {
            'name': 'Adelia',
            'phone': '+628900987',
            'address': '42 Street',
        }
        response = self.client.post('/customers/', payload)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)



