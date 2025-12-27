from django.contrib.gis.geos import Point as GeoPoint
from django.contrib.gis.measure import D
from django.contrib.gis.db.models.functions import Distance
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q

from .models import Point as LocationPoint, Message
from .serializers import (
    PointSerializer, MessageSerializer, SearchSerializer
)


class AuthenticatedAPIView(APIView):
    permission_classes = [IsAuthenticated]

# ============ POINTS API ============

class PointListCreateAPIView(AuthenticatedAPIView):
    """
    GET: Получить список всех точек
    POST: Создать новую точку
    """
    
    def get(self, request):
        """Получить список всех активных точек"""
        points = LocationPoint.objects.all()
        serializer = PointSerializer(points, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        """Создать новую точку"""
        serializer = PointSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PointSearchAPIView(AuthenticatedAPIView):
    """
    Поиск точек в заданном радиусе
    GET /api/points/search/?latitude=55.7558&longitude=37.6173&radius=10
    """
    
    def get(self, request):
        serializer = SearchSerializer(data=request.query_params)
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        
        data = serializer.validated_data
        latitude = data['latitude']
        longitude = data['longitude']
        radius_km = data['radius']
        
        # Создаем точку центра
        center_point = GeoPoint(longitude, latitude, srid=4326)
        
        # Ищем точки в радиусе
        points = LocationPoint.objects.filter(
            location__distance_lte=(center_point, D(km=radius_km))
        ).annotate(
            distance=Distance('location', center_point)
        ).order_by('distance')
        
        serializer = PointSerializer(points, many=True)
        return Response(serializer.data)

# ============ MESSAGES API ============

class MessageListCreateAPIView(AuthenticatedAPIView):
    """
    GET: Получить список всех сообщений
    POST: Создать новое сообщение
    """
    
    def get(self, request):
        """Получить список всех одобренных сообщений"""
        messages = Message.objects.all()
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        """Создать новое сообщение"""
        print("DEBUG: Получен запрос на создание сообщения")
        print(f"DEBUG: Данные: {request.data}")
        
        serializer = MessageSerializer(data=request.data)
        
        if serializer.is_valid():
            print("DEBUG: Сериализатор валиден")
            message = serializer.save()
            print(f"DEBUG: Сообщение создано с ID: {message.id}")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        print(f"DEBUG: Ошибки сериализатора: {serializer.errors}")
        return Response(
            {
                'error': 'Неверные данные',
                'details': serializer.errors,
                'received_data': request.data
            },
            status=status.HTTP_400_BAD_REQUEST
        )


class MessageDetailAPIView(AuthenticatedAPIView):
    """
    GET: Получить детали сообщения
    PUT: Обновить сообщение полностью
    PATCH: Частично обновить сообщение
    DELETE: Удалить сообщение
    """
    
    def get_object(self, pk):
        try:
            return Message.objects.get(pk=pk)
        except Message.DoesNotExist:
            return None
    
    def get(self, request, pk):
        """Получить детали сообщения"""
        message = self.get_object(pk)
        if message is None:
            return Response(
                {'error': 'Сообщение не найдено или не одобрено'},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = MessageSerializer(message)
        return Response(serializer.data)
    
    def put(self, request, pk):
        """Полное обновление сообщения"""
        message = self.get_object(pk)
        if message is None:
            return Response(
                {'error': 'Сообщение не найдено или не одобрено'},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = MessageSerializer(message, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MessageSearchAPIView(AuthenticatedAPIView):
    """
    Поиск сообщений в заданном радиусе
    GET /api/messages/search/?latitude=55.7558&longitude=37.6173&radius=10
    """
    
    def get(self, request):
        serializer = SearchSerializer(data=request.query_params)
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        
        data = serializer.validated_data
        latitude = data['latitude']
        longitude = data['longitude']
        radius_km = data['radius']
        
        # Создаем точку центра
        center_point = GeoPoint(longitude, latitude, srid=4326)
        
        # Ищем сообщения в радиусе
        messages = Message.objects.filter(
            Q(location__distance_lte=(center_point, D(km=radius_km))) |
            Q(point__location__distance_lte=(center_point, D(km=radius_km)))
        ).annotate(
            distance=Distance('location', center_point)
        ).order_by('distance')
        
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)