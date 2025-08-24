from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token

from .models import CustomUser

class RegisterSerializer(serializers.ModelSerializer):
  password = serializers.CharField(write_only=True)

  class Meta:
    model = get_user_model()
    fields = ('username', 'email', 'password', 'bio', 'profile_picture')

  def create(self, validated_data):
    user = get_user_model().objects.create_user(
      username=validated_data['username'],
      email=validated_data.get('email'),
      password=validated_data['password'],
      bio=validated_data.get('bio', ''),
      profile_picture=validated_data.get('profile_picture')
    )
    Token.objects.create(user=user)
    return user

class LoginSerializer(serializers.Serializer):
  username = serializers.CharField()
  password = serializers.CharField(write_only=True)


class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = CustomUser
    fields = ["id", "username", "email", "bio", "profile_picture"]

class TokenSerializer(serializers.ModelSerializer):
  class Meta:
    model = Token
    fields = ('key')