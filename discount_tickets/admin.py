from django.contrib import admin

from django.contrib import admin
from .models import Restaurant, Ticket, Purchase, Owner

admin.site.register(Restaurant)
admin.site.register(Ticket)
admin.site.register(Purchase)
admin.site.register(Owner)
