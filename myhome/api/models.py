from django.db import models


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

    address = models.CharField('주소', max_length=100)
    zip_code = models.IntegerField('우편번호')
    room_type = models.CharField('방 종류', max_length=10, choices=ROOM_TYPE_CHOICES)
    deposit = models.IntegerField('보증금')
    monthly_rent = models.IntegerField('월세')
    management_fee = models.IntegerField('관리비')
    total_floor = models.IntegerField('전체 층수')
    floor = models.IntegerField('층수')
    structure = models.CharField('구조', max_length=20)
    space = models.IntegerField('전용 면적')
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
    landlord_name = models.CharField('집주인 이름', max_length=10)
    landlord_contact = models.CharField('집주인 번호', max_length=20)
    sold_out = models.BooleanField('활성화', default=True)

    def __str__(self):
        return self.address


class Tenant(models.Model):
    UNIVERSITY_CHOICES = [
        ('연세대학교', '연세대학교'),
        ('이화여자대학교', '이화여자대학교'),
    ]

    GENDER_CHOICES = [
        ('남', '남'),
        ('여', '여'),
    ]

    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='tenants', verbose_name='매물')
    university = models.CharField('학교', max_length=10, choices=UNIVERSITY_CHOICES)
    gender = models.CharField('성별', max_length=5, choices=GENDER_CHOICES)
    residence_length = models.CharField('거주 기간', max_length=30, null=True, blank=True)


class Review(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='reviews', verbose_name='매물')
    pros = models.CharField('장점', max_length=40)
    cons = models.CharField('단점', max_length=40)
    comment = models.CharField('하고 싶은 말', max_length=40)
    rate = models.IntegerField('평점')


class Photo(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='photos', verbose_name='매물')
    photo_file = models.ImageField('사진', upload_to='photo/%Y/%m/%d')  # request.FIELS['image_files'] -> MEDIA_ROOT
    # path: image.image_file.path  MEDIA_ROOT/photo/~/~/~/~.jpg (절대 경로) - 경로에 저장
    # url: image.image_file.url  MEDIA_URL/photo/~/~/~/~.jpg (상대 경로) - DB에 문자열로 저장


class Contract(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='contracts', verbose_name='매물')
    contract_file = models.ImageField('계약서', upload_to='contract/%Y/%m/%d')
