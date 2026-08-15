from rest_framework.serializers import ModelSerializer
from authentication.models import Profile
from django.contrib.auth.models import User

class UserGetSerializer(ModelSerializer):
    class Meta:
        model=User
        fields=['username', 'email', 'first_name', 'last_name']

class RegisterSerializer(ModelSerializer):
    class Meta:
        model=User
        fields=['username', 'email', 'first_name', 'last_name', 'password']

class ProfileGetSerializer(ModelSerializer):
    user=UserGetSerializer(read_only=True)
    class Meta:
        model=Profile
        fields=['id', 'user', 'name', 'bio', 'created_at']

class ProfileSerializer(ModelSerializer):
    user=UserGetSerializer(read_only=True)
    class Meta:
        model=Profile
        fields='__all__'

class ProfileUpdateSerializer(ModelSerializer):
    class Meta:
        model=Profile
        fields=['bio', 'profile_pic']