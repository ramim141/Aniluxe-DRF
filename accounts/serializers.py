from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from rest_framework import serializers
from .models import UserAccount

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "first_name", "last_name", "email"]


class UserAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccount
        fields = [
            "id",
            "user",
            "image",
        ]


class UserRegistrationSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            "username",
            "password",
            "confirm_password",
            "first_name",
            "last_name",
            "email",
            "image",
        ]

    def create(self, validated_data):
        username = validated_data["username"]
        email = validated_data["email"]
        password = validated_data["password"]
        confirm_password = validated_data["confirm_password"]
        first_name = validated_data["first_name"]
        last_name = validated_data["last_name"]

        if password != confirm_password:
            raise serializers.ValidationError("Password doesn't match")

        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("Email already exists")
        elif User.objects.filter(username=username).exists():
            raise serializers.ValidationError("Username already taken")

        user = User(
            username=username, email=email, first_name=first_name, last_name=last_name
        )
        user.set_password(password)
        user.is_active = False
        user.save()
        image_data = validated_data.pop("image", "images/profile/user_avatar.png")
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)


class UserUpdateSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False)

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "image"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance:
            try:
                user_account = self.instance.account
            except UserAccount.DoesNotExist:
                user_account = None
            if user_account:
                self.fields["image"].initial = user_account.image

    def save(self, **kwargs):
        commit = kwargs.pop("commit", True)
        user_data = super().save(**kwargs)

        if commit:
            user_data.save()

            user_account, created = UserAccount.objects.get_or_create(user=user_data)
            user_account.image = self.validated_data.get("image", None)
            user_account.save()

        return user_data


class ChangePasswordSerializer(serializers.Serializer):
    user_id = serializers.IntegerField(required=True)
    old_password = serializers.CharField(write_only=True, required=True)
    password = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)

    def validate(self, attrs):
        user_id = attrs.get("user_id")
        old_password = attrs.get("old_password")
        password = attrs.get("password")
        password2 = attrs.get("password2")

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise ValidationError("User not found")

        if not user.check_password(old_password):
            raise ValidationError("Old password is not correct")

        if password != password2:
            raise ValidationError("New password fields didn't match")

        return attrs

    def save(self):
        user_id = self.validated_data["user_id"]
        password = self.validated_data["password"]

        user = User.objects.get(id=user_id)
        user.set_password(password)
        user.save()