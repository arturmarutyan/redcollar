# points/tests/test_authentication.py
from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from django.contrib.gis.geos import Point as GeoPoint
from ..models import Point, Message


class AuthenticationTestCase(TestCase):
    """Базовый класс для тестов с аутентификацией"""
    
    def setUp(self):
        """Настройка тестовых данных"""
        # Создаем тестовых пользователей
        self.user1 = User.objects.create_user(
            username='testuser1',
            email='test1@example.com',
            password='fekfekfekfek'
        )
        self.user2 = User.objects.create_user(
            username='testuser2',
            email='test2@example.com',
            password='fekfekfekfek'
        )
        self.admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='fekfekfekfek'
        )
        
        # API клиенты
        self.client = APIClient()
        self.user_client = APIClient()
        
        # Авторизуем клиентов
        self.user_client.force_authenticate(user=self.user1)
        
        # Создаем тестовые точки
        self.point1 = Point.objects.create(
            location=GeoPoint(37.6173, 55.7558, srid=4326),
        )
        
        self.point2 = Point.objects.create(
            location=GeoPoint(37.6273, 55.7658, srid=4326),
        )
        
        # Создаем тестовые сообщения
        self.message1 = Message.objects.create(
            point=self.point1,
            title='Сообщение от user1',
            content='Текст сообщения 1'
        )
        
        self.message2 = Message.objects.create(
            point=self.point2,
            title='Сообщение от user2',
            content='Текст сообщения 2'
        )