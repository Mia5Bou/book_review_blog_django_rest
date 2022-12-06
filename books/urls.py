from django.urls import path
from .views import BookView, BookDetail

urlpatterns = [
    path('', BookView.as_view()),
    path('book/<uuid:pk>/', BookDetail.as_view()),
]
