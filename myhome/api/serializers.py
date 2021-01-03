from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from django.contrib.auth.hashers import make_password
from .models import User, Mentor, Room, Review, Comment, Photo


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = '__all__'


class RoomSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    photos = PhotoSerializer(many=True, read_only=True)

    class Meta:
        model = Room
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'interest_rooms', 'email', 'password', 'name', 'contact', 'birth', 'gender']


class MentorSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)

    class Meta:
        model = Mentor
        fields = '__all__'


def get_token(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class UserLoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=64)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)
    
    def validate(self, attrs):
        email = attrs.get("email", None)
        password = attrs.get("password", None)
        user = authenticate(email=email, password=password)

        if user is None:
            return {
                'email': 'None'
            }
        try:
            token = get_token(user)
            update_last_login(None, user)
        except User.DoesNotExist:
            raise serializers.ValidationError(
                '가입되지 않은 이메일이거나, 잘못된 비밀번호입니다.'
            )
        return {
            'email': user.email,
            'token': token
        }
