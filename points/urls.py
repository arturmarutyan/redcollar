# points/urls.py
from django.urls import path
from .views import (
    # Точки
    PointListCreateAPIView,
    PointSearchAPIView,
    
    # Сообщения
    MessageListCreateAPIView,
    MessageDetailAPIView,
    MessageSearchAPIView,
)

urlpatterns = [
    # ============ ПОЛЬЗОВАТЕЛЬСКИЙ ИНТЕРФЕЙС ============
    
    # ============ ТОЧКИ ============
    # Список всех точек и создание новой
    path('points/', PointListCreateAPIView.as_view(), name='point-list-create'),
        
    # Поиск точек в радиусе
    path('points/search/', PointSearchAPIView.as_view(), name='point-search'),

    # ============ СООБЩЕНИЯ ============
    # Список всех сообщений и создание нового
    path('points/messages/', MessageListCreateAPIView.as_view(), name='message-list-create'),
    
    # Детали, обновление, удаление сообщения
    path('points/messages/<int:pk>/', MessageDetailAPIView.as_view(), name='message-detail'),
    
    # Поиск сообщений в радиусе
    path('points/messages/search/', MessageSearchAPIView.as_view(), name='message-search'),
]