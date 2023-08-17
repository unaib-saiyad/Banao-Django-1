from rest_framework import serializers
from .models import UserInformation
from django.contrib.auth.models import User


class UserValidation(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name']

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class UserInfoValidation(serializers.ModelSerializer):
    class Meta:
        model = UserInformation
        exclude = ['user', 'id']

    def create(self, validated_data):
        return UserInformation.objects.create(**validated_data)
