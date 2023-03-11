from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import ROLE_CHOICES
from .models import User, USER


class RegistrationSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())],
    )
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())],
    )

    class Meta:
        model = User
        fields = ("email", "username")

    def validate_username(self, username):
        username = username.lower()
        if username == "me":
            raise serializers.ValidationError(
                f'You cannot use "{username}" as username.'
            )
        return username

    def validate_username_email(self, username, email):
        email = email.lower()
        if User.objects.filter(email=email, username=username).exists():
            raise serializers.ValidationError(
                f"User with username {username} and email {email} already "
                f"exists."
            )
        return username, email


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)
    role = serializers.ChoiceField(
        choices=ROLE_CHOICES, default=USER, initial=USER
    )


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    role = serializers.ChoiceField(
        choices=ROLE_CHOICES, default=USER, initial=USER
    )

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "bio",
            "role",
        )
        read_only_fields = ("role",)
