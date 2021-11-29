from django import db
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
import rest_framework

from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse("user:create")
CREATE_TOKEN_URL = reverse("user:token")
ME_URL = reverse("user:me")


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicUserApiTest(TestCase):
    """Test the User's API public endpoint"""

    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user_success(self):
        """Test creating user with valid paylaod is successful"""
        payload = {
            "email": "test@testtest.email",
            "name": "Steve Test",
            "password": "testpass",
        }

        response = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**response.data)
        self.assertTrue(user.check_password(payload["password"]))
        self.assertNotIn("password", response.data)

    def test_user_already_exist_return_bad_request(self):
        """Test creating a user that already exist returns a bad request"""
        payload = {"email": "test@test.com", "password": "testpass"}
        create_user(**payload)

        response = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short_returns_bad_request(self):
        """Test creating a user with a password too short returns a bad request"""
        payload = {"email": "test@test.com", "password": "pw"}

        response = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(email=payload["email"]).exists()
        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        """Test that a token is created for the user"""
        payload = {
            "email": "token@testtest.email",
            "password": "testpass123",
        }
        create_user(**payload)

        response = self.client.post(CREATE_TOKEN_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("token", response.data)

    def test_create_token_with_invalid_credential_fails(self):
        """Test that creating a token with invalid login creds fails"""
        create_user(email="derp@blerp.com", password="flerp123")
        payload = {
            "email": "derp@blerp.com",
            "password": "testwrongpass",
        }

        response = self.client.post(CREATE_TOKEN_URL, payload)

        self._assert_token_creation_failed(response)

    def test_create_token_for_non_existing_user_fails(self):
        """Test that creating a token for a user that does not exist fails"""
        payload = {
            "email": "derp@blerp.com",
            "password": "test_pass",
        }

        response = self.client.post(CREATE_TOKEN_URL, payload)

        self._assert_token_creation_failed(response)

    def test_create_token_with_missing_password_fails(self):
        """Test creating a token without providing a password fails"""
        create_user(email="derp@blerp.com", password="flerp123")
        payload = {
            "email": "derp@blerp.com",
        }

        response = self.client.post(CREATE_TOKEN_URL, payload)

        self._assert_token_creation_failed(response)

    def test_authentication_is_required_on_me_endpoint(self):
        """Test that authentication is required to access /me endpoint"""
        response = self.client.get(ME_URL)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # Assertion helpers
    def _assert_token_creation_failed(self, response):
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn("token", response.data)


class PrivateUserApiTests(TestCase):
    """Test private endpoints of the user api"""

    def setUp(self):
        self.user = create_user(
            email="test@derp.com",
            password="TestTest1",
            name="Derp",
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_profile_success(self):
        """test retrieve a profile successfully"""
        response = self.client.get(ME_URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data,
            {
                "email": self.user.email,
                "name": self.user.name,
            },
        )

    def test_me_not_allowed(self):
        """test that POST are not allowed on the /me endpoint"""
        response = self.client.post(ME_URL, {})

        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile(self):
        """test that a user can update its profile through the /me endpoint"""
        new_name = "Flupr"
        response = self.client.patch(ME_URL, {"name": new_name})

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.user.refresh_from_db()
        self.assertEqual(self.user.name, new_name)
