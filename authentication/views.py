from users.models import *
from users.serializers import *
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth import login, logout
from django.contrib.auth.hashers import make_password


class LoginView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'authentication/login.html'

    def get(self, request):
        return Response(status=status.HTTP_200_OK)

    def post(self, request):
        try :
            user = UserData.objects.get(email=request.data['email'])
            if not user.check_password(request.data['password']):
                messages.error(request, f"Wrong email address or password")
                return Response({'email' : request.data['email']}, status=status.HTTP_400_BAD_REQUEST)

            login(request, user)
            return redirect(f"/users/profile/{user.username}")

        except UserData.DoesNotExist:
            messages.error(request, f"Wrong email address or password")
            return Response({'email' : request.data['email']}, status=status.HTTP_400_BAD_REQUEST)
 


class LogoutView(APIView):

    def get(self, request):
        messages.info(request, f"You have been logged out")
        logout(request)
        return redirect('reviews-view')


class RegisterView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'authentication/register.html'

    def get(self, request):
        return Response(status=status.HTTP_200_OK)

    def post(self, request):
        # 1. WE START BY CREATING THE USER
        if request.data['password'] != request.data['password2']:
            messages.error(request, f"Passwords do not match.")
            return Response(request.data, status=status.HTTP_400_BAD_REQUEST)

        user_data = {
            'username' : request.data['username'],
            'email'    : request.data['email'],
            'password' : make_password(request.data['password']),
        }
        user_serializer = UserRegistrationSerializer(data=user_data)
        if not user_serializer.is_valid():
            for field in user_serializer.errors:
                for error in user_serializer.errors[field]:
                    if error.code == 'unique':
                        messages.error(request, f"The {field} '{request.data[field]}' has already been taken")
                    elif error.code == 'blank':
                        messages.error(request, f"The field '{field}' is required")
                    else :
                        messages.error(request, f"An error has occured")
            return Response(request.data, status=status.HTTP_400_BAD_REQUEST)

        user = user_serializer.save()
        
        # 2. NOW WE CREATE THE PROFILE
        profile_data = {
                'user'       : user_serializer.data['id'],
                'first_name' : request.data['first_name'],
                'last_name'  : request.data['last_name'],
                'bio'        : request.data['bio'],
        }

        if request.data['picture'] != '':
                profile_data['picture'] = request.FILES.get('picture')

        profile_serializer = ProfileSerializer(data=profile_data)
        if not profile_serializer.is_valid():
            user.delete()
            for field in profile_serializer.errors:
                for error in profile_serializer.errors[field]:
                    if error.code == 'unique':
                        messages.error(request, f"The {field} '{request.data[field]}' has already been taken")
                    elif error.code == 'blank':
                        messages.error(request, f"The field '{field}' is required")
                    elif error.code == 'invalid_image':
                        messages.error(request, str(error))
                    else :
                        messages.error(request, f"An error has occured")
            return Response(request.data, status=status.HTTP_400_BAD_REQUEST)
 
        profile_serializer.save()

        login(request, user)

        return redirect(f"/users/profile/{user_serializer.data['username']}")