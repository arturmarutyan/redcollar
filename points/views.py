
from django.contrib.gis.geos import Point as GeoPoint
from django.contrib.gis.measure import D
from django.contrib.gis.db.models.functions import Distance
from rest_framework import viewsets, generics, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
import math

from .models import Point, Message
from .serializers import (
    PointSerializer, MessageSerializer, SearchSerializer
)
from .filters import MessageFilter


class PointViewSet(viewsets.ModelViewSet):
    """
    API для работы с точками
    """
    queryset = Point.objects.all()
    serializer_class = PointSerializer
    
    @action(detail=False, methods=['get'], url_path='search')
    def search_in_radius(self, request):
        """
        Поиск точек в заданном радиусе
        GET /api/points/search/?latitude=55.75&longitude=37.61&radius=10
        """
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
        
        center_point = GeoPoint(longitude, latitude, srid=4326)
        
        # Ищем точки в радиусе
        queryset = Point.objects.filter(
            location__distance_lte=(center_point, D(km=radius_km)),
        ).annotate(
            distance=Distance('location', center_point)
        ).order_by('distance')
        
        # Сериализуем результат
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = PointSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = PointSerializer(queryset, many=True)
        return Response(serializer.data)
    
    # @action(detail=True, methods=['get'], url_path='messages')
    # def point_messages(self, request, pk=None):
    #     """
    #     Получение сообщений для конкретной точки
    #     GET /api/points/{id}/messages/
    #     """
    #     point = self.get_object()
    #     messages = point.messages.filter()
        
    #     page = self.paginate_queryset(messages)
    #     if page is not None:
    #         serializer = MessageSerializer(page, many=True)
    #         return self.get_paginated_response(serializer.data)
        
    #     serializer = MessageSerializer(messages, many=True)
    #     return Response(serializer.data)


class MessageViewSet(viewsets.ModelViewSet):
    """
    API для работы с сообщениями
    """
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = MessageFilter
    
    def perform_create(self, serializer):
        # Автоматически устанавливаем местоположение из точки, если не указано
        point = serializer.validated_data['point']
        if not serializer.validated_data.get('location') and point:
            serializer.validated_data['location'] = point.location
        serializer.save()
    
    @action(detail=False, methods=['get'], url_path='search')
    def search_messages(self, request):
        """
        Поиск сообщений в заданном радиусе
        GET /api/points/messages/search/?latitude=55.7558&longitude=37.6173&radius=10
        """
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
        
        # Ищем сообщения в радиусе (по местоположению сообщения)
        queryset = Message.objects.filter(
            Q(location__distance_lte=(center_point, D(km=radius_km))) |
            Q(point__location__distance_lte=(center_point, D(km=radius_km))),
        ).annotate(
            distance=Distance('location', center_point)
        ).order_by('distance')
        
        # Сериализуем результат
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = MessageSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = MessageSerializer(queryset, many=True)
        return Response(serializer.data)