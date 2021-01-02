from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views


router = DefaultRouter()
router.register(r'rooms', views.RoomViewSet)
router.register(r'reviews', views.ReviewViewSet)
router.register(r'photos', views.PhotoViewSet)
router.register(r'comments', views.CommentViewSet)
router.register(r'users', views.UserViewSet)
router.register(r'mentors', views.MentorViewSet)

urlpatterns = router.urls
