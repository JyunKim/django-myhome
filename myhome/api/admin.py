from django.contrib import admin
from .models import Room, Tenant, Review, Photo, Contract

admin.site.register(Room)
admin.site.register(Tenant)
admin.site.register(Review)
admin.site.register(Photo)
admin.site.register(Contract)
