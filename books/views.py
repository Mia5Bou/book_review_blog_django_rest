from .models import Book
from .serializers import BookSerializer
from users.models import UserData, Profile
from reviews.models import Review
from reviews.serializers import ReviewSerializer
from django.http import Http404
from django.shortcuts import redirect
from django.db.models import Q
from reviews.models import Review
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer
import os


class BookView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'books/books.html'

    def get(self, request, format=None):
        books = Book.objects.all()
        data_queryparams = request.query_params
        response_dict = dict()
        if 'search' in data_queryparams :
            response_dict['keyword'] = data_queryparams['search']
            response_dict['search_by'] = data_queryparams['search_by']
            if data_queryparams['search_by'] == 'all' :
                    books = books.filter(Q(title__icontains=data_queryparams['search']) 
                               | Q(author__pen_name__icontains=data_queryparams['search'])
                               | Q(author__user__first_name__icontains=data_queryparams['search'])
                               | Q(author__user__last_name__icontains=data_queryparams['search']))
            elif data_queryparams['search_by'] == 'title' :
                    books = books.filter(Q(title__icontains=data_queryparams['search']))
            elif data_queryparams['search_by'] == 'summary' :
                    books = books.filter(Q(summary__icontains=data_queryparams['search']))
            elif data_queryparams['search_by'] == 'author' :
                    books = books.filter(Q(author__pen_name__icontains=data_queryparams['search'])
                                       | Q(author__user__first_name__icontains=data_queryparams['search'])
                                       | Q(author__user__last_name__icontains=data_queryparams['search']))
        response_dict['books'] = books.order_by('title')

        return Response(response_dict, status=status.HTTP_200_OK)


class BookDetail(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'books/book.html'

    def get_object(self, pk):
        try:
            return Book.objects.get(pk=pk)
        except:
            raise Http404

    def get(self, request, pk, format=None):
        book = self.get_object(pk)
        book_reviews = Review.objects.filter(book=book).order_by('-date_added')
        return Response({'book' : book, 'book_reviews' : book_reviews, 'path_right' : os.path.exists(book.cover.url)}, status=status.HTTP_200_OK)

    def post(self, request, pk, format=None):
        profile = Profile.objects.get(user=UserData.objects.get(username=request.user))
        data = {
            'content' : request.data['content'],
            'book'    : pk,
            'profile' : profile.id,
        }
        serializer = ReviewSerializer(data=data)

        book = self.get_object(pk)
        book_reviews = Review.objects.filter(book=book).order_by('-date_added')
        data = {'book' : book, 'book_reviews' : book_reviews, 'path_right' : os.path.exists(book.cover.url)}

        if serializer.is_valid():
            serializer.save()
            return Response(data, status=status.HTTP_200_OK)

        return Response(data, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk, format=None):
        book = self.get_object(pk)
        serializer = BookSerializer(book, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        book = self.get_object(pk)
        book.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)