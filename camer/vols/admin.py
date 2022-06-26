from django.contrib import admin

from .models import  Vols, Airport, Passenger
# Register your models here.
admin.site.register(Airport)
admin.site.register(Vols)
admin.site.register(Passenger)