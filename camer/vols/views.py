from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .models import Vols, Passenger, Airport

# Create your views here.
def index(request):
    return render(request, "vols/index.html", {
        "vols": Vols.objects.all()
    })

def vol(request, vol_id):
    vol = Vols.objects.get(pk= vol_id)
    return render(request, "vols/vol.html", {
        "vol": vol,
        "passengers": vol.passengers.all(),
        "non_passengers": Passenger.objects.exclude(vols=vol).all()
    })

def book(request, vol_id):
    if request.method == "POST":
        vol = Vols.objects.get(pk=vol_id)
        passenger = Passenger.objects.get(pk= int(request.POST["passenger"]))
        passenger.vols.add(vol)
        return HttpResponseRedirect(reverse("vol", args=(vol_id,)))