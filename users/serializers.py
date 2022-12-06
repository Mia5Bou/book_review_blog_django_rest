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
        fields = ['first_name', 'last_name']


class UserInfoUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserData
        fields = ['username', 'email']


class ProfilePictureUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['picture']



# class ProfileRegisterFormSerializer(serializers.Serializer):
#     username = serializers.CharField(
#         max_length=50,
#         allow_blank=False,
#         required=True,
#     )
#     email = serializers.EmailField(
#         max_length=100,
#         allow_blank=True,
#         required=True,
#     )
#     password = serializers.CharField(
#         max_length=100,
#         style={'input_type': 'password'},
#         allow_blank=True,
#         required=False,
#     )
#     first_name = serializers.CharField(
#         max_length=100,
#         allow_blank=True,
#         required=False,
#     )
#     last_name = serializers.CharField(
#         max_length=100,
#         required=False,
#         allow_blank=True,
#     )
#     picture = serializers.ImageField(
#         use_url=True,
#         # max_length=None,
#         required=False,
#         # default = None,
#         # allow_empty_file=True,
#         default='default_user.jpg',
#         # default='',
#     )
#     bio = serializers.CharField(
#         allow_blank=True,
#         style={'base_template': 'textarea.html'},
#         required=False,
#     )