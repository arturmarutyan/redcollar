from rest_framework import status
from ..models import Point
from .test_authentication import AuthenticationTestCase


class PointAPITestCase(AuthenticationTestCase):
    """Тесты для эндпоинтов точек"""
        
    def test_get_points_list_authenticated(self):
        """Публичный доступ к списку точек"""
        response = self.user_client.get('/api/points/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.json()), 0)
    
    def test_get_points_list_unauthenticated(self):
        """Ограниченный доступ к списку точек"""
        response = self.client.get('/api/points/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


    def test_search_points_authenticated(self):
        """Публичный доступ к поиску точек"""
        response = self.user_client.get(
            '/api/points/search/',
            {'latitude': 55.7558, 'longitude': 37.6173, 'radius': 10}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_create_point_authenticated(self):
        """Создание точки авторизованным пользователем"""
        data = {
            'latitude': 55.7580,
            'longitude': 37.6200,
        }
        
        response = self.user_client.post('/api/points/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Проверяем данные в ответе
        response_data = response.json()
        self.assertEqual(response_data['latitude'], data['latitude'])
        
    
    def test_create_point_unauthenticated(self):
        """Попытка создания точки без авторизации"""
        data = {
            'latitude': 55.75,
            'longitude': 37.62
        }
        
        response = self.client.post('/api/points/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_create_point_invalid_data(self):
        """Создание точки с невалидными данными"""
        # Без координат
        data = {'bad': 'request'}
        response = self.user_client.post('/api/points/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        # С невалидными координатами
        data = {
            'latitude': 'nan',
            'longitude': 37.62
        }
        response = self.user_client.post('/api/points/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
