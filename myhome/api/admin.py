from django.contrib import admin
from .models import Account, Room, Review, Comment, Photo

admin.site.register(Account)
admin.site.register(Room)
admin.site.register(Review)
admin.site.register(Comment)
admin.site.register(Photo)
