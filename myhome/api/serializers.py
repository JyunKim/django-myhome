from rest_framework import serializers
from .models import Account, Appointment, Room, Review, Photo


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'


class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = '__all__'


class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = '__all__'


class RoomSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)
    photos = PhotoSerializer(many=True, read_only=True)

    class Meta:
        model = Room
        fields = '__all__'
