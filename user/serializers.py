from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import ugettext_lazy as t

from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the User object"""

    class Meta:
        model = get_user_model()
        fields = (
            "email",
            "name",
            "password",
        )
        extra_kwargs = {
            "password": {
                "write_only": True,
                "min_length": 5,
            }
        }

    def create(self, validated_data):
        """create a new user encrypted password and return it"""
        return get_user_model().objects.create_user(**validated_data)


class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the user authentication object"""

    email = serializers.CharField()
    password = serializers.CharField(
        style={"input_type": "password"},
        trim_whitespace=False,
    )

    def validate(self, attrs):
        """Validate and authenticate the user"""
        email = attrs.get("email")
        password = attrs.get("password")

        user = authenticate(
            request=self.context.get("request"), username=email, password=password
        )

        if not user:
            message = t("Unable to authenticate with provide credential")
            raise serializers.ValidationError(message, code="authentication")

        attrs["user"] = user
        return attrs
