from rest_framework import serializers
from .models import User, Room, Review, Comment, Photo


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
    interest_rooms = RoomSerializer(many=True, read_only=True)
    rooms = RoomSerializer(many=True, read_only=True)
    reviews = ReviewSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'interest_rooms', 'email', 'name', 'contact', 'birth', 'gender', 'rooms', 'reviews']
