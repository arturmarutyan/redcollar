# Django REST API

Для запуска: поставить виртуальное окружение   
git clone https://github.com/arturmarutyan/redcollar.git  
python3 -m venv .venv  
source .venv/bin/activate  
pip install -r requirements.txt # в корне проекта  
Добавить файл .env с SECRET_KEY  
python manage.py makemigrations  
python manage.py migrate  
python manage.py runserver  

Данный проект позволяет пользователям оставлять на карте любые замечания и читать чужие. Так, например, можно  
оставить отзыв на свой любимый ресторан или почитать отзывы других о месте, которое собираешься посетить.  

# Эндпоинты  

curl -X POST http://localhost:8000/auth/token/ \  
  -H "Content-Type: application/json" \  
  -d '{  
    "username": "your_username",  
    "password": "your_password"  
  }'  

Ответ: {
    'refresh': '...',
    'access': '...'
}  

curl -X POST http://localhost:8000/auth/register/ \  
  -H "Content-Type: application/json" \  
  -d '{  
    "username": "your_username",  
    'email': 'user@example.com',  
    'password1': 'your_password',  
    "password2": "your_password"  
  }'  

Ответ: {
    'refresh': '...',
    'access': '...'
}  

curl -X POST http://localhost:8000/auth/token/refresh/ \  
  -H "Content-Type: application/json" \  
  -d '{  
    'refresh': '...'
  }'  

Ответ: {
    'access': '...'
}  

curl -X GET http://localhost:8000/api/points/ \  
  -H "Authorization: Bearer $ACCESS_TOKEN" \  
  -H "Content-Type: application/json"  

Ответ: [
    {'id': 1, 'location', '...', 'latitude': 23.00, 'longitude': 24.00},
]  

curl -X POST http://localhost:8000/api/points/ \  
  -H "Authorization: Bearer $ACCESS_TOKEN" \  
  -H "Content-Type: application/json"  
  -d '{  
    'latitude': 23.00,  
    'longitude': 24.00,  
  }'  

Ответ: {
    'id': 1, 'location', '...', 'latitude': 23.00, 'longitude': 24.00
}  


curl -X GET http://localhost:8000/api/points/search/?latitude=23.00&longitude=24.00&radius=10 \  
  -H "Authorization: Bearer $ACCESS_TOKEN" \  
  -H "Content-Type: application/json"  

Ответ: [
    {'id': 1, 'location', '...', 'latitude': 23.00, 'longitude': 24.00},
]  

curl -X GET http://localhost:8000/api/points/messages/ \  
  -H "Authorization: Bearer $ACCESS_TOKEN" \  
  -H "Content-Type: application/json"  

Ответ: [
    {'point': 1, 'title', '...', 'content': '...', 'location': '...'},
]  


curl -X POST http://localhost:8000/api/points/messages/ \  
  -H "Authorization: Bearer $ACCESS_TOKEN" \  
  -H "Content-Type: application/json" 
  -d {'point': 1, 'title': 'first', 'content': 'all good'} 

Ответ:  


curl -X GET http://localhost:8000/api/points/messages/search?latitude=23.00&longitude=24.00&radius=10 \  
  -H "Authorization: Bearer $ACCESS_TOKEN" \  
  -H "Content-Type: application/json"  

Ответ:  [
    {'point': 1, 'title', '...', 'content': '...', 'location': '...'},
]

