from django.contrib import admin
from .models import User, Mentor, Room, Review, Comment, Photo, Reservation

admin.site.register(User)
admin.site.register(Mentor)
admin.site.register(Room)
admin.site.register(Review)
admin.site.register(Comment)
admin.site.register(Photo)
admin.site.register(Reservation)
