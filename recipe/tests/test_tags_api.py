from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Tag

from recipe.serializers import TagSerializer


TAGS_URL = reverse("recipe:tag-list")


class PublicTagsApiTests(TestCase):
    """Test the public tags api"""

    def setUp(self) -> None:
        self.client = APIClient()

    def test_login_required(self):
        """test login is required for tags api"""
        response = self.client.get(TAGS_URL)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTagsApiTest(TestCase):
    """Test private tags endpoints"""

    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user("test@test.com", "password1!")
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_tags(self):
        """Test retrieving tags"""
        Tag.objects.create(user=self.user, name="vegan")
        Tag.objects.create(user=self.user, name="dessert")

        response = self.client.get(TAGS_URL)

        tags = Tag.objects.all().order_by("-name")
        serializer = TagSerializer(tags, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_tags_limited_to_logged_in_user(self):
        """test that tags returned are limited to the logged in user"""
        other_user = get_user_model().objects.create_user(
            "paul@paul.com", "uiuiuiuiuiu"
        )
        tag = Tag.objects.create(user=self.user, name="vegan")
        Tag.objects.create(user=other_user, name="dessert")

        response = self.client.get(TAGS_URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["name"], tag.name)

    def test_create_tag_successful(self):
        """test create a tag"""
        payload = {"name": "test tag"}
        response = self.client.post(TAGS_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        exists = Tag.objects.filter(
            user=self.user,
            name=payload["name"],
        ).exists()
        self.assertTrue(exists)

    def test_create_tag_invalid(self):
        """test create tag fails when name is empty"""
        payload = {"name": ""}
        response = self.client.post(TAGS_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
