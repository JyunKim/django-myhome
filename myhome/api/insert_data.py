# manage.py shell -> from api import insert_data
from .models import User, Mentor, Room, Review, Comment


user1 = User.objects.create(
    email='a@a.com',
    password='1234',
    name='세입자',
    contact='01012341234',
    birth='1997-11-11',
    gender='여성'
)

user2 = User.objects.create(
    email='b@b.com',
    password='1234',
    name='집주인',
    contact='01023452345',
    birth='1965-03-20',
    gender='여성'
)

mentor = Mentor.objects.create(
    name='멘토',
    email='mentor@gmail.com',
    contact='01038754782',
    birth='1981-05-22',
    gender='남성',
    region='서대문구 연희동',
    introduction='안녕하세요, 공인중개사 2년차입니다.',
    career='공인중개사 자격증'
)

room = Room.objects.create(
    user=user2,
    address='서울특별시 서대문구 연세로 50',
    address_detail='122동 301호',
    zip_code='03722',
    room_type='원룸',
    deposit=1000,
    monthly_rent=50,
    management_fee=5,
    total_floor=5,
    floor=3,
    structure='일반',
    space=20,
    completion_year=2010,
    elevator=True,
    bed=True,
    desk=True,
    refrigerator=True,
    induction=True,
    air_conditioner=True,
    washer=True,
    short_term=False,
    heating='중앙난방',
    occupancy_date='2021-01-10',
    introduction='이만한 집이 없습니다~',
    detail='남향이고 햇빛 잘 들어옵니다. 수압 좋고, 온수 잘 나옵니다.',
    distance='연세대학교 서문 5분 거리',
    latitude=37.564089,
    longitude=126.9367922
)

review = Review.objects.create(
    user=user1,
    mentor=mentor,
    content='너무 친절하시고 좋았습니다.',
    rate='5.0'
)

comment = Comment.objects.create(
    user=user1,
    room=room,
    pros='학교랑 가깝습니다.',
    cons='방음이 잘 안됩니다.',
    content='전반적으로 괜찮습니다.',
    rate='4.5'
)
