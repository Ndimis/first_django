from django.urls import path
from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("<int:vol_id>", views.vol, name="vol"),
    path("<int:vol_id>/book", views.book, name="book")
]