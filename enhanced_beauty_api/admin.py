from django.contrib import admin
from .models import Service, Client, Visit, VisitService, Booking, Availability

admin.site.register(Service)
admin.site.register(Client)
admin.site.register(Visit)
admin.site.register(VisitService)
admin.site.register(Booking)
admin.site.register(Availability)
