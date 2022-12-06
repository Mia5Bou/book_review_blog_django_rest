from django.urls import path
from .views import *


urlpatterns = [
    path('profiles/', ProfileView.as_view(), name='profile-list'),
    path('profile/<str:username>/', ProfileDetail.as_view(), name='profile-view'),

    path('authors/', AuthorView.as_view()),
    path('author/<str:username>/', AuthorDetail.as_view()),
]