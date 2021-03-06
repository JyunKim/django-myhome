import os
import base64
import hmac
import hashlib
import time
import json
import requests
import datetime
from random import randint
from django import forms
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.core.mail import send_mail
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('사용자의 이메일이 없습니다.')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('관리자가 아닙니다.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('관리자가 아닙니다.')
        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    GENDER_CHOICES = [
        ('남성', '남성'),
        ('여성', '여성'),
    ]

    interest_rooms = models.ManyToManyField('Room', related_name='users', verbose_name='관심 매물', blank=True)
    email = models.EmailField('이메일', unique=True)
    name = models.CharField('이름', max_length=20)
    contact = models.CharField('휴대폰 번호', max_length=20)
    birth = models.DateField('생년월일', blank=True, null=True)
    gender = models.CharField('성별', max_length=5, choices=GENDER_CHOICES)
    is_staff = models.BooleanField(_('staff status'), default=False)
    is_active = models.BooleanField(_('active'), default=True)

    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        return self.name

    def get_full_name(self):
        return self.name

    def get_short_name(self):
        return self.name

    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)


class Mentor(models.Model):
    GENDER_CHOICES = [
        ('남성', '남성'),
        ('여성', '여성'),
    ]

    name = models.CharField('이름', max_length=20)
    email = models.EmailField('이메일', unique=True)
    contact = models.CharField('휴대폰 번호', max_length=20)
    birth = models.DateField('생년월일', blank=True, null=True)
    gender = models.CharField('성별', max_length=5, choices=GENDER_CHOICES)
    region = models.CharField('지역', max_length=20)
    introduction = models.CharField('한줄 소개', max_length=40)
    career = models.CharField('경력', max_length=100)

    def __str__(self):
        return self.name


class Room(models.Model):
    ROOM_TYPE_CHOICES = [
        ('원룸', '원룸'),
        ('투룸', '투룸'),
        ('쓰리룸', '쓰리룸'),
    ]

    HEATING_CHOICES = [
        ('중앙난방', '중앙난방'),
        ('개별난방', '개별난방'),
    ]

    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='rooms', verbose_name='집주인')
    name = models.CharField('이름', max_length=30)
    address = models.CharField('주소', max_length=50)
    address_detail = models.CharField('상세주소', max_length=50)
    zip_code = models.CharField('우편번호', max_length=10)
    room_type = models.CharField('방 종류', max_length=10, choices=ROOM_TYPE_CHOICES)
    deposit = models.IntegerField('보증금')
    monthly_rent = models.IntegerField('월세')
    management_fee = models.IntegerField('관리비')
    total_floor = models.IntegerField('전체 층수')
    floor = models.IntegerField('층수')
    space = models.FloatField('전용 면적')
    completion_year = models.IntegerField('준공연도')
    elevator = models.BooleanField('엘레베이터')
    bed = models.BooleanField('침대')
    desk = models.BooleanField('책상')
    refrigerator = models.BooleanField('냉장고')
    induction = models.BooleanField('인덕션')
    air_conditioner = models.BooleanField('에어컨')
    washer = models.BooleanField('세탁기')
    short_term = models.BooleanField('단기 임대')
    heating = models.CharField('난방', max_length=10, choices=HEATING_CHOICES)
    occupancy_date = models.DateField('입주 가능일')
    introduction = models.CharField('한 줄 소개', max_length=30)
    detail = models.TextField('상세 설명')
    distance = models.CharField('거리', max_length=40, null=True, blank=True)
    activation = models.BooleanField('활성화', default=True)
    latitude = models.FloatField('위도')
    longitude = models.FloatField('경도')

    def __str__(self):
        return self.address


def rate_validator(value):
    if value < 0 or value > 5:
        raise forms.ValidationError('0 ~ 5 사이의 숫자를 입력해주세요.')


class Reservation(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='reservations', verbose_name='예약자')
    room = models.ForeignKey('Room', on_delete=models.CASCADE, related_name='reserves', verbose_name='매물')
    date = models.DateTimeField('예약 날짜')
    complete = models.BooleanField('예약 완료 여부', default=False)


class Review(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='written_reviews', verbose_name='작성자')
    mentor = models.ForeignKey('Mentor', on_delete=models.CASCADE, related_name='reviews', verbose_name='멘토')
    content = models.TextField('후기')
    rate = models.FloatField('평점', validators=[rate_validator])


class Comment(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='comments', verbose_name='작성자')
    room = models.ForeignKey('Room', on_delete=models.CASCADE, related_name='comments', verbose_name='매물')
    pros = models.CharField('장점', max_length=40)
    cons = models.CharField('단점', max_length=40)
    content = models.CharField('한줄 평', max_length=40)
    rate = models.FloatField('평점', validators=[rate_validator])


class Photo(models.Model):
    room = models.ForeignKey('Room', on_delete=models.CASCADE, related_name='photos', verbose_name='매물')
    photo_file = models.ImageField('사진', upload_to='photo/%Y/%m/%d')
    # request.data = request.POST + request.FILES
    # request.FIELS['photo_file'] -> MEDIA_ROOT
    # path: photo.photo_file.path  MEDIA_ROOT/photo/~/~/~/~.jpg (절대 경로) - 경로에 저장
    # url: photo.photo_file.url  MEDIA_URL/photo/~/~/~/~.jpg (상대 경로) - DB에 문자열로 저장


# 상대경로 - manage.py 기준
with open('./config/secrets.json') as secret_file:
    secrets = json.load(secret_file)


class SMSAuth(models.Model):
    phone_number = models.CharField('휴대폰 번호', max_length=20, primary_key=True)
    auth_number  = models.IntegerField('인증 번호')
    updated_at = models.DateTimeField('인증 일시', auto_now=True)

    def save(self, *args, **kwargs):
        self.auth_number = randint(100000, 1000000)
        super().save(*args, **kwargs)
        self.send_sms()

    def	make_signature(self, message):
        secret_key = secrets["NCP_SECRET_KEY"]
        secret_key = bytes(secret_key, 'UTF-8')
        signingKey = base64.b64encode(hmac.new(secret_key, message, digestmod=hashlib.sha256).digest())
        return signingKey

    def send_sms(self):
        timestamp = int(time.time() * 1000)
        timestamp = str(timestamp)
        access_key = secrets["NCP_ACCESS_KEY"]
        method = "POST"
        uri = f'/sms/v2/services/{secrets["NCP_SENS_ID"]}/messages'

        message = method + " " + uri + "\n" + timestamp + "\n" + access_key
        message = bytes(message, 'UTF-8')
        signature = self.make_signature(message)

        header = {
            "Content-Type": "application/json; charset=utf-8",
            "x-ncp-apigw-timestamp": timestamp,
            "x-ncp-iam-access-key": access_key,
            "x-ncp-apigw-signature-v2": signature
        }

        body = {
            "type": "SMS",
            "from": secrets["PHONE_NUMBER"],
            "content": f"[마이홈] 본인확인 인증번호 [{self.auth_number}]를 입력해주세요.",
            "messages": [
                {"to": self.phone_number}
            ]
        }
        # content type이 json이므로 dumps 해줘야 함
        requests.post("https://sens.apigw.ntruss.com"+uri, data=json.dumps(body), headers=header)

    @classmethod
    def check_auth_number(cls, phone_num, auth_num):
        time_limit = timezone.now() - datetime.timedelta(minutes=3)
        result = cls.objects.filter(
            phone_number=phone_num,
            auth_number=auth_num,
            updated_at__gte=time_limit
        )
        if result:
            return '정상적으로 인증되었습니다.'
        return '인증에 실패하였습니다.'
