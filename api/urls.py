from django.urls import path
from .views import ask_view, train_view, search_view, feeds_view

urlpatterns = [
    path("ask/", ask_view),
    path("train/", train_view),
    path("search/", search_view),
    path("feeds/", feeds_view),
]
