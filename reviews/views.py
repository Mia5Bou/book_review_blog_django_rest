from .models import Review
from .serializers import ReviewSerializer
from books.models import Book
from users.models import Profile, UserData
from django.contrib import messages
from django.shortcuts import redirect
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer


class ReviewView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'reviews/reviews.html'

    def get(self, request):
        reviews = Review.objects.all().order_by('-date_added')
        books = Book.objects.all().order_by('title')
        return Response({'reviews' : reviews, 'books' : books}, status=status.HTTP_200_OK)

    def post(self, request):
        if 'update-review-content' in request.data:
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

        else:
            profile = Profile.objects.get(user=UserData.objects.get(username=request.user))
            data = {
                'content' : request.data['content'],
                'book'    : request.data['book'],
                'profile' : profile.id,
            }
            serializer = ReviewSerializer(data=data)
            if not serializer.is_valid():
                messages.error(request, f"An error has occured")
                return redirect('reviews-view')

            serializer.save()
            messages.info(request, f"Review added succesfully")

        return redirect('reviews-view')


class AboutView(APIView):
    pass