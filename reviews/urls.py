from django.urls import path
from .views import *


urlpatterns = [
    path('', ReviewView.as_view(), name='reviews-view'),

    # path('home/', HomeView.as_view(), name='home'),
    path('about/', AboutView.as_view(), name='about'),
    
]
