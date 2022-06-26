from http.client import HTTPResponse
from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.
def index(request):
    return render(request, "hello/index.html")

def ndimis(request):
    return HttpResponse("Hello Ndimis !")

def greets(request, name):
    return HttpResponse(f"Hello {name.capitalize()}")

def salutations(request, nom):
    return render(request, "hello/salutations.html",
    {
        "name" : nom.capitalize(),
    })