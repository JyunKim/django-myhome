from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views


router = DefaultRouter()
router.register(r'rooms', views.RoomViewSet)
router.register(r'reviews', views.ReviewViewSet)
router.register(r'tenants', views.TenantViewSet)
router.register(r'photos', views.PhotoViewSet)

urlpatterns = router.urls
