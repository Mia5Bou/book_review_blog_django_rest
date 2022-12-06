from .models import Review
from .serializers import ReviewSerializer
from books.models import Book
from users.models import Profile, UserData
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
        profile = Profile.objects.get(user=UserData.objects.get(username=request.user))
        data = {
            'content' : request.data['content'],
            'book'    : request.data['book'],
            'profile' : profile.id,
        }
        serializer = ReviewSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return redirect('reviews-view')

        reviews = Review.objects.all().order_by('-date_added')
        books = Book.objects.all().order_by('title')
        return Response({'errors' : serializer.errors, 'reviews' : reviews, 'books' : books, 'content' : data['content']}, status=status.HTTP_400_BAD_REQUEST)


class ReviewDetail(APIView):
    pass
    # def get_object(self, pk):
    #     try:
    #         return Review.objects.get(pk=pk)
    #     except:
    #         raise Http404

    # def get(self, request, pk, format=None):
    #     review = self.get_object(pk=pk)
    #     serializer = ReviewSerializer(review)
    #     return Response(serializer.data, status=status.HTTP_200_OK)

    # def put(self, request, pk, format=None):
    #     review = self.get_object(pk=pk)
    #     serializer = ReviewSerializer(review, data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_200_OK)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def delete(self, request, pk, format=None):
    #     review = self.get_object(pk=pk)
    #     review.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)


class AboutView(APIView):
    pass