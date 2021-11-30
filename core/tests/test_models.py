from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models


def sample_user(email="test@test.com", password="password!"):
    """Create a sample user"""
    return get_user_model().objects.create_user(email, password)


class ModelTests(TestCase):
    def test_create_user_with_email_successful(self):
        """test creating a new user with an email is successful"""
        email = "test@test.com"
        password = "testpass123"
        user = get_user_model().objects.create_user(email=email, password=password)

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Email for a new user is normalized"""
        email = "BilP@BlooPP.coM"

        user = get_user_model().objects.create_user(email, "Bloop1123")

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """Test creating user with no email raise error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, "bloop")

    def test_create_new_superuser(self):
        """test creating new superuser"""
        user = get_user_model().objects.create_superuser("super@user.com", "boopBoop")

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_tag_str(self):
        """test tag string representation"""
        tag = models.Tag.objects.create(
            user=sample_user(),
            name="Vegan",
        )

        self.assertEqual(str(tag), tag.name)
