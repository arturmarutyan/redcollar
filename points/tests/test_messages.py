from rest_framework import status
from ..models import Message
from .test_authentication import AuthenticationTestCase


class MessageAPITestCase(AuthenticationTestCase):
    """Тесты для эндпоинтов сообщений"""
        
    def test_get_messages_list_authenticated(self):
        """Публичный доступ к списку сообщений"""
        response = self.user_client.get('/api/points/messages/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.json()), 0)
    
    def test_get_messages_list_unauthenticated(self):
        """Ограниченный доступ к списку сообщений"""
        response = self.client.get('/api/points/messages/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_search_messages(self):
        """Публичный доступ к поиску сообщений"""
        response = self.user_client.get(
            '/api/points/messages/search/',
            {'latitude': 55.7558, 'longitude': 37.6173, 'radius': 10}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        
    def test_create_message_authenticated(self):
        """Создание сообщения авторизованным пользователем"""
        data = {
            'point': self.point1.id,
            'title': 'Новое тестовое сообщение',
            'content': 'Текст нового сообщения',
        }
        
        response = self.user_client.post('/api/points/messages/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Проверяем данные в ответе
        response_data = response.json()
        self.assertEqual(response_data['title'], data['title'])
        
        # Проверяем что сообщение создалось в БД
        self.assertTrue(Message.objects.filter(title=data['title']).exists())
    
    def test_create_message_unauthenticated(self):
        """Попытка создания сообщения без авторизации"""
        data = {
            'point': self.point1.id,
            'title': 'Неавторизованное сообщение',
            'content': 'Текст'
        }
        
        response = self.client.post('/api/points/messages/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_create_message_for_nonexistent_point(self):
        """Создание сообщения для несуществующей точки"""
        data = {
            'point': 99999,  # Несуществующий ID
            'title': 'Сообщение',
            'content': 'Текст'
        }
        
        response = self.user_client.post('/api/points/messages/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_create_message_without_title(self):
        """Создание сообщения без обязательных полей"""
        data = {
            'point': self.point1.id,
            'content': 'Текст без заголовка'
        }
        
        response = self.user_client.post('/api/points/messages/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        data = {
            'point': self.point1.id,
            'title': 'Текст без наполнения'
        }
        
        response = self.user_client.post('/api/points/messages/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        data = {
            'title': 'effle',
            'content': 'Текст без ключа'
        }
        
        response = self.user_client.post('/api/points/messages/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
