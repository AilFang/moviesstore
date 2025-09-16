from django.urls import path
from . import views

urlpatterns = [
    path("", views.movie_requests, name="movie_requests"),
]