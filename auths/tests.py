import json

from django.contrib.auth.models import User

from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase


class AuthTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='test1',
            password='test1',
            email='test1@mail.com'
        )
        self.token = Token.objects.get(user=self.user)

    def test_create_user(self):
        user = User.objects.create_user(username='test', password='test')
        tokens = Token.objects.filter(user=user)
        expect = True
        self.assertEqual(expect, tokens.exists())

    def test_login_success(self):
        payload = {
            'username': 'test1',
            'password': 'test1'
        }

        expect = {
            "token": self.token.key,
            "user_id": 1,
            "email": "test1@mail.com"
        }

        response = self.client.post('/auth/login/', payload, format='json')
        self.assertDictEqual(json.loads(response.content), expect)

    def test_login_failed(self):
        payload = {
            'username': 'tester',
            'password': 'anything'
        }

        expect = {
            "non_field_errors": ["Unable to log in with provided credentials."]
        }
        response = self.client.post('/auth/login/', payload)
        self.assertEqual(json.loads(response.content), expect)
