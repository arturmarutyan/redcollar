# auth_app/tests/test_auth.py
from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status


class AuthAPITestCase(TestCase):
    """Тесты для эндпоинтов аутентификации"""
    
    def setUp(self):
        self.client = APIClient()
        self.user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'lilkodakboss',
            'password2': 'lilkodakboss'
        }
    
    def test_register_success(self):
        """Успешная регистрация пользователя"""
        response = self.client.post('/auth/register/', self.user_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('access', response.json())
        self.assertIn('refresh', response.json())
        
        # Проверяем что пользователь создан
        self.assertTrue(User.objects.filter(username='testuser').exists())
    
    def test_register_password_mismatch(self):
        """Регистрация с несовпадающими паролями"""
        data = self.user_data.copy()
        data['password2'] = 'DifferentPassword123'
        
        response = self.client.post('/auth/register/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password', response.json())
    
    def test_register_duplicate_username(self):
        """Регистрация с существующим username"""
        # Создаем первого пользователя
        self.client.post('/auth/register/', self.user_data, format='json')
        
        # Пытаемся создать второго с тем же username
        data2 = self.user_data.copy()
        data2['email'] = 'another@example.com'
        
        response = self.client.post('/auth/register/', data2, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_login_success(self):
        """Успешный вход"""
        # Сначала регистрируем
        self.client.post('/auth/register/', self.user_data, format='json')
        
        # Затем логинимся
        login_data = {
            'username': 'testuser',
            'password': 'lilkodakboss'
        }
        
        response = self.client.post('/auth/token/', login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.json())
        self.assertIn('refresh', response.json())
    
    def test_login_wrong_password(self):
        """Вход с неверным паролем"""
        # Регистрируем
        self.client.post('/auth/register/', self.user_data, format='json')
        
        # Пытаемся войти с неправильным паролем
        login_data = {
            'username': 'testuser',
            'password': 'WrongPassword'
        }
        
        response = self.client.post('/auth/token/', login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_refresh_token(self):
        """Обновление токена"""
        # Регистрируем и получаем refresh token
        register_response = self.client.post('/auth/register/', self.user_data, format='json')
        refresh_token = register_response.json()['refresh']
        
        # Обновляем токен
        refresh_data = {'refresh': refresh_token}
        response = self.client.post('/auth/token/refresh/', refresh_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.json())
