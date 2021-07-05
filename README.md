# Myhome API

### Room
- URL: api/rooms/
- Method: GET, POST(로그인 필요)
- POST시 body에 id, comments, photos, activation, user를 제외한 정보 전송
```python
[
    {
        "id": 1,
        "comments": [
            {
                "id": 1,
                "pros": "학교랑 가깝다.",
                "cons": "방음이 안된다.",
                "content": "집주인분 친절하시고 집도 큰 문제 없이 좋습니다.",
                "rate": 4.5,
                "user": 2,
                "room": 1
            }
        ],
        "photos": [
            {
                "id": 1,
                "photo_file": "http://127.0.0.1:8000/media/photo/2021/01/03/CAM00525.jpg",
                "room": 1
            }
        ],
        "address": "서울특별시 서대문구 연세로 50",
        "zip_code": "03722",
        "room_type": "원룸",
        "deposit": 1000,
        "monthly_rent": 50,
        "management_fee": 5,
        "total_floor": 3,
        "floor": 2,
        "structure": "일반",
        "space": 20,
        "completion_year": 2010,
        "elevator": true,
        "bed": true,
        "desk": true,
        "refrigerator": true,
        "induction": true,
        "air_conditioner": true,
        "washer": true,
        "short_term": false,
        "heating": "중앙난방",
        "occupancy_date": "2021-01-03",
        "introduction": "이만한 집이 없어요~",
        "detail": "연세대학교 서문에서 가깝고, 학생들이 많이 이용했었습니다!",
        "distance": "연세대학교 서문 5분 거리",
        "activation": true,
        "user": 3
    }
]
```

- URL: api/rooms/{room_id}/
- Method: GET, PUT(로그인 필요), DELETE(로그인 필요)
```python
{
    "id": 1,
    "comments": [
        {
            "id": 1,
            "pros": "학교랑 가깝다.",
            "cons": "방음이 안된다.",
            "content": "집주인분 친절하시고 집도 큰 문제 없이 좋습니다.",
            "rate": 4.5,
            "user": 2,
            "room": 1
        }
    ],
    "photos": [
        {
            "id": 1,
            "photo_file": "http://127.0.0.1:8000/media/photo/2021/01/03/CAM00525.jpg",
            "room": 1
        }
    ],
    "address": "서울특별시 서대문구 연세로 50",
    "zip_code": "03722",
    "room_type": "원룸",
    "deposit": 1000,
    "monthly_rent": 50,
    "management_fee": 5,
    "total_floor": 3,
    "floor": 2,
    "structure": "일반",
    "space": 20,
    "completion_year": 2010,
    "elevator": true,
    "bed": true,
    "desk": true,
    "refrigerator": true,
    "induction": true,
    "air_conditioner": true,
    "washer": true,
    "short_term": false,
    "heating": "중앙난방",
    "occupancy_date": "2021-01-03",
    "introduction": "이만한 집이 없어요~",
    "detail": "연세대학교 서문에서 가깝고, 학생들이 많이 이용했었습니다!",
    "distance": "연세대학교 서문 5분 거리",
    "activation": true,
    "user": 3
}
```

Filter
- URL: api/rooms/?room_type=원룸&room_type=투룸&deposit_min=1&deposit_max=1000&monthly_rent_min=1&monthly_rent_max=50&management_fee_min=1&management_fee_max=5&space_min=1&space_max=10
- Method: GET   
![filter](myhome/api/img/filter.PNG)

Nested list
- URL: api/rooms/{room_id}/comment-list/
- Method: GET
```python
[
    {
        "id": 1,
        "pros": "학교랑 가깝다.",
        "cons": "방음이 안된다.",
        "content": "집주인분 친절하시고 집도 큰 문제 없이 좋습니다",
        "rate": 4.5,
        "user": 2,
        "room": 1
    }
]
```

- URL: api/rooms/{room_id}/post-comment/
- Method: POST
- body에 pros, cons, content, rate 정보 전송
```python
{
    "id": 1,
    "pros": "학교랑 가깝다.",
    "cons": "방음이 안된다.",
    "content": "집주인분 친절하시고 집도 큰 문제 없이 좋습니다",
    "rate": 4.5,
    "user": 2,
    "room": 1
}
```

- URL: api/rooms/{room_id}/photo-list/
- Method: GET
```python
[
    {
        "id": 1,
        "photo_file": "/media/photo/2021/01/01/CAM00376.jpg",
        "room": 1
    }
]
```

- URL: api/rooms/{room_id}/post-photo/
- Method: POST
- body에 photo_file 정보 전송
```python
{
    "id": 1,
    "photo_file": "/media/photo/2021/01/01/CAM00376.jpg",
    "room": 1
}
```
  
### User
- URL: api/users/
- Method: GET, POST
```python
[
    {
        "id": 1,
        "interest_rooms": [],
        "email": "kann1997@naver.com",
        "password": "pbkdf2_sha256$180000$cD2Rkdelv4CG$QDPenmqj4/+f6k31GxCNDA7QkSkBe6qp+X3MCbspc9Q=",
        "name": "",
        "contact": "",
        "birth": null,
        "gender": ""
    },
    {
        "id": 2,
        "interest_rooms": [
            1
        ],
        "email": "asdf@naver.com",
        "password": "qwer1234",
        "name": "김호미",
        "contact": "01012341234",
        "birth": "2021-01-03",
        "gender": "여성"
    },
    {
        "id": 3,
        "interest_rooms": [],
        "email": "qwer@naver.com",
        "password": "qwer1234",
        "name": "집주인",
        "contact": "01023452345",
        "birth": "1973-05-15",
        "gender": "여성"
    }
]
```

- URL: api/users/{user_id}
- Method: GET, PUT(본인만 가능), DELETE(본인만 가능)
```python
{
    "id": 2,
    "interest_rooms": [
        1
    ],
    "email": "asdf@naver.com",
    "password": "qwer1234",
    "name": "김호미",
    "contact": "01012341234",
    "birth": "2021-01-03",
    "gender": "여성"
}
```

Nested list
- URL: api/users/{user_id}/interest-room-list/
- Method: GET
```python
[
    {
        "id": 1,
        "comments": [
            {
                "id": 1,
                "pros": "학교랑 가깝다.",
                "cons": "방음이 안된다.",
                "content": "집주인분 친절하시고 집도 큰 문제 없이 좋습니다.",
                "rate": 4.5,
                "user": 2,
                "room": 1
            }
        ],
        "photos": [
            {
                "id": 1,
                "photo_file": "http://127.0.0.1:8000/media/photo/2021/01/03/CAM00525.jpg",
                "room": 1
            }
        ],
        "address": "서울특별시 서대문구 연세로 50",
        "zip_code": "03722",
        "room_type": "원룸",
        "deposit": 1000,
        "monthly_rent": 50,
        "management_fee": 5,
        "total_floor": 3,
        "floor": 2,
        "structure": "일반",
        "space": 20,
        "completion_year": 2010,
        "elevator": true,
        "bed": true,
        "desk": true,
        "refrigerator": true,
        "induction": true,
        "air_conditioner": true,
        "washer": true,
        "short_term": false,
        "heating": "중앙난방",
        "occupancy_date": "2021-01-03",
        "introduction": "이만한 집이 없어요~",
        "detail": "연세대학교 서문에서 가깝고, 학생들이 많이 이용했었습니다!",
        "distance": "연세대학교 서문 5분 거리",
        "activation": true,
        "user": 3
    }
]
```

- URL: api/users/{user_id}/reservation-list/
- Method: GET
```python
[
    {
        "id": 1,
        "room_name": "asdf",
        "room_type": "원룸",
        "room_deposit": 1,
        "room_monthly_rent": 1,
        "room_management_fee": 1,
        "room_floor": 1,
        "room_space": 1.0,
        "date": "2021-02-25T23:37:35",
        "complete": false,
        "user": 1,
        "room": 1
    }
]
```

### Mentor
- URL: api/mentors/
- Method: GET, POST(로그인 필요)
```python
[
    {
        "id": 1,
        "reviews": [
            {
                "id": 1,
                "content": "너무 친절하게 잘 설명해주셔서 좋았습니다.",
                "rate": 5.0,
                "user": 2,
                "mentor": 1
            }
        ],
        "name": "메멘토",
        "email": "zxcv@gmail.com",
        "contact": "01034563456",
        "birth": "1980-10-22",
        "gender": "남성",
        "region": "서대문구 신촌동",
        "introduction": "안전한 직거래 도와드리겠습니다",
        "career": "공인중개사 자격증"
    }
]
```

- URL: api/mentors/{mentor_id}/
- Method: GET, PUT(로그인 필요), DELETE(로그인 필요)
- 생략

Nested list
- URL: api/mentors/{mentor_id}/review-list/
- Method: GET
```python
[
    {
        "id": 1,
        "content": "너무 친절하게 잘 설명해주셔서 좋았습니다.",
        "rate": 5.0,
        "user": 2,
        "mentor": 1
    }
]
```

- URL: api/mentors/{mentor_id}/post-review/
- Method: POST
- body에 content, rate 정보 전송
```python
{
    "id": 1,
    "content": "너무 친절하게 잘 설명해주셔서 좋았습니다.",
    "rate": 5.0,
    "user": 2,
    "mentor": 1
}
```

### Review
- URL: api/reviews/
- Method: GET, POST(로그인 필요)
```python
[
    {
        "id": 1,
        "content": "너무 친절하게 잘 설명해주셔서 좋았습니다.",
        "rate": 5.0,
        "user": 2,
        "mentor": 1
    }
]
```

- URL: api/reviews/{review_id}/
- Method: GET, PUT(로그인 필요), DELETE(로그인 필요)
- 생략

### Comment
- URL: api/comments/
- Method: GET, POST(로그인 필요)
```python
[
    {
        "id": 1,
        "pros": "학교랑 가깝다.",
        "cons": "방음이 안된다.",
        "content": "집주인분 친절하시고 집도 큰 문제 없이 좋습니다.",
        "rate": 4.5,
        "user": 2,
        "room": 1
    }
]
```

- URL: api/comments/{comment_id}/
- Method: GET, PUT(로그인 필요), DELETE(로그인 필요)
- 생략

### Photo
- URL: api/photos/
- Method: GET, POST
```python
[
    {
        "id": 1,
        "photo_file": "http://127.0.0.1:8000/media/photo/2021/01/03/CAM00525.jpg",
        "room": 1
    }
]
```

- URL: api/photos/{photo_id}/
- Method: GET, PUT(로그인 필요), DELETE(로그인 필요)
- 생략

### Login
- URL: api/login/
- Method: POST   
email, password -> token 발행
```python
{
    "email": "zxcv@naver.com",
    "password": "qwer1234"
}
```
```python
{
    "message": "success",
    "token": "{'refresh': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYwOTg1MjM2NiwianRpIjoiZjIzNjBmOTI4NzNjNGUxNzg0YjNlY2JlYzZiNGM5ZDQiLCJ1c2VyX2lkIjo3fQ.erP3l2NqAH3D_20aJdhQofpXZ2VAGxBrp4vmrZHaYMU', 'access': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjA5NzY5NTY2LCJqdGkiOiI0NDFlNjJkMGRkMGY0NzcyYTZlZDYzN2M3NTRlOWVhMSIsInVzZXJfaWQiOjd9.kARZC5ttxoq2KiYcEl7S5HyCyPGuR3uIgRWXxYkhy3g'}"
}
```

### Interest room
- URL: api/interest-rooms/{room_id}/
- Method: POST(로그인 필요)
- 성공 시 status 200, 실패 시 status 400 반환

### Kakao login
- URL: api/kakao-login/

### SMS authentication
- URL: api/users/auth/
1. 휴대폰 번호 입력 -> 문자 발송
- Method: POST
- phone_number
2. 인증번호 입력
- Method: GET
- phone_number, auth_number

### Password reset
1. 이메일 입력 -> 비밀번호 초기화 링크 전송
- URL: api/password-reset/
- Method: POST
- email
2. 새 비밀번호 입력
