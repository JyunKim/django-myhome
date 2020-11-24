from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Room, Tenant, Review, Photo, Contract
from .serializers import RoomSerializer, TenantSerializer, ReviewSerializer, PhotoSerializer, ContractSerializer


class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
