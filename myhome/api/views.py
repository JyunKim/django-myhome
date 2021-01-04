from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend, filters, FilterSet
from django.shortcuts import get_object_or_404
from .models import User, Mentor, Room, Review, Comment, Photo
from .serializers import UserSerializer, MentorSerializer, RoomSerializer, ReviewSerializer, CommentSerializer, PhotoSerializer, UserLoginSerializer


class RoomFilter(FilterSet):
    room_type = filters.MultipleChoiceFilter(choices=Room.ROOM_TYPE_CHOICES)
    deposit = filters.RangeFilter()
    monthly_rent = filters.RangeFilter()
    management_fee = filters.RangeFilter()
    space_min = filters.NumberFilter(field_name='space', method='filter_space_gte')
    space_max = filters.NumberFilter(field_name='space', method='filter_space_lte')
    
    def filter_space_gte(self, queryset, name, value):
        return queryset.filter(space__gte=int(value)*3.305785)

    def filter_space_lte(self, queryset, name, value):
        return queryset.filter(space__lte=int(value)*3.305785)


class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    filterset_class = RoomFilter

    @action(detail=True, url_path='comment-list')
    def comment_list(self, request, pk):
        room = get_object_or_404(Room, pk=pk)
        comments = room.comments.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    @action(detail=True, url_path='photo-list')
    def photo_list(self, request, pk):
        room = get_object_or_404(Room, pk=pk)
        photos = room.photos.all()
        serializer = PhotoSerializer(photos, many=True)
        return Response(serializer.data)


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class PhotoViewSet(viewsets.ModelViewSet):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class MentorViewSet(viewsets.ModelViewSet):
    queryset = Mentor.objects.all()
    serializer_class = MentorSerializer

    @action(detail=True, url_path='review-list')
    def review_list(self, request, pk):
        mentor = get_object_or_404(Mentor, pk=pk)
        reviews = mentor.reviews.all()
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    if request.method == 'POST':
        serializer = UserLoginSerializer(data=request.data)

        if not serializer.is_valid(raise_exception=True):
            return Response({'message': 'Request Body Error.'}, status=status.HTTP_409_CONFLICT)
        if serializer.validated_data['email'] == 'None':
            return Response({'message': 'fail'}, status=status.HTTP_400_BAD_REQUEST)

        response = {
            'message': 'success',
            'token': serializer.data['token']
        }
        return Response(response, status=status.HTTP_200_OK)
