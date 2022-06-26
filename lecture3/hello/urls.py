from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("ndimis", views.ndimis, name="ndimis"),
    #path("<str:name>", views.greets, name="greets"),
    path("<str:nom>", views.salutations, name="salutations"),
]