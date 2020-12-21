from django.contrib import admin
from .models import Account, Appointment, Room, Review, Photo

admin.site.register(Account)
admin.site.register(Appointment)
admin.site.register(Room)
admin.site.register(Review)
admin.site.register(Photo)
