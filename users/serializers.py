from .models import UserData, Profile, Author
from rest_framework import serializers


class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserData
        fields = ('id', 'username', 'email', 'password', 'is_superuser')
        extra_kwargs = {'password' : {'write_only' : True}}

    def create(self, validated_data):
        user = UserData.objects.create(**validated_data)
        return user


class SuperUserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserData
        fields = ('id', 'username', 'email', 'password', 'is_superuser')
        extra_kwargs = {'password' : {'write_only' : True}}

    def create(self, validated_data):
        user = UserData.objects.create_superuser(**validated_data)
        return user


class UserDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserData
        fields = ('id', 'username', 'email', 'password', 'is_superuser')


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'


class ProfileInfoUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'bio']


class UserInfoUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserData
        fields = ['username', 'email']


class ProfilePictureUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['picture']