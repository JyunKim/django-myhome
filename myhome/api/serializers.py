from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from django.contrib.auth.hashers import make_password
from .models import User, Mentor, Room, Review, Comment, Photo, Reservation


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    user_email = serializers.SerializerMethodField()
    user_birth = serializers.SerializerMethodField()
    user_gender = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = '__all__'

    def get_user_email(self, obj):
        return obj.user.email
    
    def get_user_birth(self, obj):
        return obj.user.birth

    def get_user_gender(self, obj):
        return obj.user.gender


class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = '__all__'


class RoomSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    photos = PhotoSerializer(many=True, read_only=True)
    user_name = serializers.SerializerMethodField()
    user_contact = serializers.SerializerMethodField()

    class Meta:
        model = Room
        fields = '__all__'
    
    def get_user_name(self, obj):
        return obj.user.name

    def get_user_contact(self, obj):
        return obj.user.contact


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'interest_rooms', 'email', 'password', 'name', 'contact', 'birth', 'gender']

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data['email'],
            name=validated_data['name'],
            contact=validated_data['contact'],
            birth=validated_data['birth'],
            gender=validated_data['gender'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class MentorSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)

    class Meta:
        model = Mentor
        fields = '__all__'


class UserLoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=64)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)
    
    def get_token(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)

    def validate(self, attrs):
        email = attrs.get("email", None)
        password = attrs.get("password", None)
        user = authenticate(email=email, password=password)

        if user is None:
            return {
                'email': 'None'
            }
        try:
            token = self.get_token(user)
            update_last_login(None, user)
        except User.DoesNotExist:
            raise serializers.ValidationError(
                '가입되지 않은 이메일이거나, 잘못된 비밀번호입니다.'
            )
        return {
            'email': user.email,
            'token': token
        }


class ReservationSerializer(serializers.ModelSerializer):
    room_name = serializers.SerializerMethodField()
    room_type = serializers.SerializerMethodField()
    room_deposit = serializers.SerializerMethodField()
    room_monthly_rent = serializers.SerializerMethodField()
    room_management_fee = serializers.SerializerMethodField()
    room_floor = serializers.SerializerMethodField()
    room_space = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = '__all__'

    def get_room_name(self, obj):
        return obj.room.name
    
    def get_room_type(self, obj):
        return obj.room.room_type
    
    def get_room_deposit(self, obj):
        return obj.room.deposit

    def get_room_monthly_rent(self, obj):
        return obj.room.monthly_rent
    
    def get_room_management_fee(self, obj):
        return obj.room.management_fee
    
    def get_room_floor(self, obj):
        return obj.room.floor
    
    def get_room_space(self, obj):
        return obj.room.space
