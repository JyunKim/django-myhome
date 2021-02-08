import json
from rest_framework import status, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly, BasePermission, SAFE_METHODS
from rest_framework_simplejwt.tokens import RefreshToken
from django_filters.rest_framework import DjangoFilterBackend, filters, FilterSet
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, resolve_url
from django.contrib.auth import authenticate
from django.contrib.auth.views import PasswordResetView, PasswordResetCompleteView
from .models import User, Mentor, Room, Review, Comment, Photo, SMSAuth
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
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def create(self, request, *args, **kwargs):
        request.data['user'] = request.user.id
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(detail=True, url_path='comment-list')
    def comment_list(self, request, pk):
        room = get_object_or_404(Room, pk=pk)
        comments = room.comments.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)
    
    @action(methods=['post'], detail=True, url_path='post-comment')
    def post_comment(self, request, pk):
        request.data['user'] = request.user.id
        request.data['room'] = pk
        serializer = CommentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(detail=True, url_path='photo-list')
    def photo_list(self, request, pk):
        room = get_object_or_404(Room, pk=pk)
        photos = room.photos.all()
        serializer = PhotoSerializer(photos, many=True)
        return Response(serializer.data)

    @action(methods=['post'], detail=True, url_path='post-photo')
    def post_photo(self, request, pk):
        request.data['room'] = pk
        room = get_object_or_404(Room, pk=pk)
        for file in request.FILES.getlist('photo_file'):
            request.data['photo_file'] = file
            serializer = PhotoSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
        serializer = RoomSerializer(room)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def create(self, request, *args, **kwargs):
        request.data['user'] = request.user.id
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def create(self, request, *args, **kwargs):
        request.data['user'] = request.user.id
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class PhotoViewSet(viewsets.ModelViewSet):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def create(self, request, *args, **kwargs):
        serializers = []
        for file in request.FILES.getlist('photo_file'):
            request.data['photo_file'] = file
            serializer = PhotoSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            serializers.append(serializer.data)
            headers = self.get_success_headers(serializer.data)
        return Response(serializers, status=status.HTTP_201_CREATED, headers=headers)


class ProfileUpdatePermission(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj == request.user


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (ProfileUpdatePermission,)

    @action(detail=True, url_path='interest-room-list')
    def interest_room_list(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        rooms = user.interest_rooms.all()
        serializer = RoomSerializer(rooms, many=True)
        return Response(serializer.data)


class MentorViewSet(viewsets.ModelViewSet):
    queryset = Mentor.objects.all()
    serializer_class = MentorSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    @action(detail=True, url_path='review-list')
    def review_list(self, request, pk):
        mentor = get_object_or_404(Mentor, pk=pk)
        reviews = mentor.reviews.all()
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)

    @action(methods=['post'], detail=True, url_path='post-review')
    def post_review(self, request, pk):
        request.data['user'] = request.user.id
        request.data['mentor'] = pk
        serializer = ReviewSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        
        
@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    if request.method == 'POST':
        serializer = UserLoginSerializer(data=request.data)

        if not serializer.is_valid(raise_exception=True):
            return Response({'message': 'fail'}, status=status.HTTP_409_CONFLICT)
        if serializer.validated_data['email'] == 'None':
            return Response({'message': 'fail'}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(email=request.data["email"], password=request.data["password"])
        user_serializer = UserSerializer(user)
        response = {
            'message': 'success',
            'token': serializer.data['token'],
            'user': user_serializer.data
        }
        return Response(response, status=status.HTTP_200_OK)


# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def logout(request):
#     if request.method == 'POST':
#         try:
#             refresh_token = request.data["refresh"]
#             token = RefreshToken(refresh_token)
#             token.blacklist()
#             return Response(status=status.HTTP_205_RESET_CONTENT)
#         except Exception as e:
#             return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def interest_room(request, room_id):
    room = get_object_or_404(Room, pk=room_id)
    user = request.user

    if room in user.interest_rooms.all():
        user.interest_rooms.remove(room)
        return Response({'message': 'OK'}, status=status.HTTP_200_OK)
    else:
        user.interest_rooms.add(room)
        return Response({'message': 'OK'}, status=status.HTTP_200_OK)
    return Response({'message': 'Bad Request'}, status=status.HTTP_400_BAD_REQUEST)


class SMSAuthView(APIView):
    # 인증 번호 입력
    def get(self, request):
        try:
            phone_num = request.query_params['phone_number']
            auth_num = request.query_params['auth_number']
            result = SMSAuth.check_auth_number(phone_num, auth_num)
            return Response({'message': 'OK', 'result': result})
        except KeyError:
            return Response({'message': 'Bad Request'}, status=status.HTTP_400_BAD_REQUEST)
        
    # 휴대폰 번호 입력
    def post(self, request):
        try:
            phone_num = request.data['phone_number']
            SMSAuth.objects.update_or_create(phone_number=phone_num)  # 업데이트, 없으면 생성 -> save() 실행
            return Response({'message': 'OK'})
        except KeyError:
            return Response({'message': 'Bad Request'}, status=status.HTTP_400_BAD_REQUEST)


class UserPasswordResetView(PasswordResetView):
    email_template_name = 'registration/password_reset.html'
    subject_template_name = 'registration/password_reset.txt'

    def form_valid(self, form):
        if User.objects.get(email=self.request.POST.get('email')):
            return super().form_valid(form)
        else:
            return Response({'message': 'Bad Request'}, status=status.HTTP_400_BAD_REQUEST)


class UserPasswordResetCompleteView(PasswordResetCompleteView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['login_url'] = resolve_url('login')
        return context
