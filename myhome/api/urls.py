from django.urls import path, include
from django.contrib.auth import views as auth_views
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from . import views


router = DefaultRouter()
router.register(r'rooms', views.RoomViewSet)
router.register(r'reviews', views.ReviewViewSet)
router.register(r'photos', views.PhotoViewSet)
router.register(r'comments', views.CommentViewSet)
router.register(r'users', views.UserViewSet)
router.register(r'mentors', views.MentorViewSet)

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # email, password
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # refresh: refresh token
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),  # token: token
    path('login/', views.login, name='login'),
    # path('logout/', views.logout, name='logout'),
    path('kakao-login/', views.kakao_login, name='kakao_login'),
    path('kakao-login/token/', views.get_kakao_token, name='kakao_token'),
    path('interest-rooms/<int:room_id>/', views.interest_room, name='interest_room'),
    path('users/auth/', views.SMSAuthView.as_view(), name='user_auth'),
    path('password-reset/', views.UserPasswordResetView.as_view(), name='password_reset'),
    path('password-reset-done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password-reset-complete/', views.UserPasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('', include(router.urls)),
]
