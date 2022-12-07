from .models import Profile, Author
from .serializers import *
from reviews.models import Review
from reviews.serializers import ReviewSerializer
from books.models import Book
from django.http import Http404
from django.db.models import Q
from django.shortcuts import redirect
from django.contrib import messages
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.renderers import TemplateHTMLRenderer


class ProfileView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'users/profiles.html'

    def get(self, request):
        profiles = Profile.objects.all().order_by('user__username')
        data_queryparams = request.query_params
        if 'search' in data_queryparams :
            profiles = profiles.filter(Q(user__first_name__icontains=data_queryparams['search'])
                                     | Q(user__last_name__icontains=data_queryparams['search'])
                                     | Q(user__username__icontains=data_queryparams['search']))
        return Response({'profiles' : profiles}, status=status.HTTP_200_OK)


class ProfileDetail(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'users/profile.html'

    def get_object(self, username):
        try:
            return Profile.objects.get(user=UserData.objects.get(username=username))
        except:
            raise Http404

    def get(self, request, username):
        profile = self.get_object(username)
        reviews = Review.objects.filter(profile=profile).order_by('-date_added')
        books = Book.objects.all().order_by('title')
        return Response({'profile' : profile, 'reviews' : reviews, 'books' : books}, status=status.HTTP_200_OK)

    def post(self, request, username):
        profile = self.get_object(username)

        if all(key in request.data for key in ['first_name', 'last_name', 'username', 'email']):
            user_serializer = UserInfoUpdateSerializer(profile.user, data=request.data)
            if not user_serializer.is_valid():
                for field in user_serializer.errors:
                    for error in user_serializer.errors[field]:
                        if error.code == 'unique':
                            messages.error(request, f"The {field} '{request.data[field]}' has already been taken")
                        elif error.code == 'blank':
                            messages.error(request, f"The field '{field}' is required")
                        else:
                            messages.error(request, f"An error has occured")

                return redirect(f"/users/profile/{username}")

            profile_serializer = ProfileInfoUpdateSerializer(profile, data=request.data)
            if not profile_serializer.is_valid():
                messages.error(request, f"An error has occured")
                return redirect(f"/users/profile/{username}")

            user_serializer.save()
            profile_serializer.save()
            messages.info(request, f"Profile updated successfully")

        elif all(key in request.data for key in ['content', 'book']):
            # Posting a new review
            data = {
                'content' : request.data['content'],
                'book'    : request.data['book'],
                'profile' : profile.id,
            }
            serializer = ReviewSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                messages.info(request, f"Review added successfully")
        
        elif 'picture' in request.data:
            # Modifying the profile picture
                serializer = ProfilePictureUpdateSerializer(profile, data={'picture' : request.FILES.get('picture')})

                if serializer.is_valid():
                    profile.picture.delete(save=True)
                    serializer.save()
                    messages.info(request, f"Profile picture updated successfully")

        elif 'delete_picture' in request.data:
            # Deleting the profile picture
            profile.picture.delete(save=True)
            profile.picture = Profile._meta.get_field('picture').get_default()
            profile.save()
            messages.info(request, f"Profile picture deleted successfully")

        elif 'update-review-content' in request.data:
            review = Review.objects.get(pk=request.data['id'])
            serializer = ReviewSerializer(review, data=request.data, partial=True)

            if not serializer.is_valid():
                messages.error(request, f"An error has occured")
                return redirect('reviews-view')

            serializer.save()
            messages.info(request, f"Review updated succesfully")

        elif 'delete-review' in request.data:
            review = Review.objects.get(pk=request.data['id'])
            review.delete()
            messages.info(request, f"Review deleted succesfully")

        return redirect(f"/users/profile/{username}")


    def put(self, request, username):
        profile = self.get_object(username)
        serializer = ProfileSerializer(profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, username):
        profile = self.get_object(username)
        profile.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AuthorView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'users/authors.html'

    def get(self, request):
        authors = Author.objects.all().order_by('pen_name')
        data_queryparams = request.query_params
        if 'search' in data_queryparams :
            authors = authors.filter(Q(pen_name__icontains=data_queryparams['search']))
        return Response({'authors' : authors}, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = AuthorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AuthorDetail(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'users/author.html'

    def get_object(self, username):
        try:
            return Author.objects.get(user__username=username)
        except:
            raise Http404

    def get(self, request, username):
        response_dict = {'match_pen_name' : False}
        author = self.get_object(username)
        response_dict['author'] = author
        if author.pen_name == author.user.first_name+' '+author.user.last_name:
            response_dict['match_pen_name'] = True
        books = Book.objects.filter(author=author)
        response_dict['books'] = books
        return Response(response_dict, status=status.HTTP_200_OK)

    def put(self, request, username):
        profile = self.get_object(username=username)
        serializer = AuthorSerializer(profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, username):
        profile = self.get_object(username=username)
        profile.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)