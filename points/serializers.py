# points/serializers.py
from rest_framework import serializers
from django.contrib.gis.geos import Point as GeoPoint
from .models import Point, Message


class PointSerializer(serializers.ModelSerializer):
    latitude = serializers.FloatField(
        write_only=True,
        required=True,
        help_text="Широта"
    )
    longitude = serializers.FloatField(
        write_only=True,
        required=True,
        help_text="Долгота"
    )
    
    class Meta:
        model = Point
        fields = [
            'id', 'latitude', 'longitude', 'location',
        ]
        read_only_fields = ['id', 'location']
    
    def validate_latitude(self, value):
        """Валидация широты"""
        if isinstance(value, str) and value.lower() == 'nan':
            raise serializers.ValidationError("Latitude cannot be NaN")
        if not (-90 <= value <= 90):
            raise serializers.ValidationError("Latitude must be between -90 and 90")
        return value
    
    def validate_longitude(self, value):
        """Валидация долготы"""
        if isinstance(value, str) and value.lower() == 'nan':
            raise serializers.ValidationError("Longitude cannot be NaN")
        if not (-180 <= value <= 180):
            raise serializers.ValidationError("Longitude must be between -180 and 180")
        return value

    def create(self, validated_data):
        # Извлекаем координаты
        latitude = validated_data.pop('latitude')
        longitude = validated_data.pop('longitude')
        
        # Создаем Point объект (GeoDjango)
        # Важно: Point принимает (longitude, latitude)
        location = GeoPoint(longitude, latitude, srid=4326)
        
        # Создаем объект модели
        point = Point.objects.create(
            location=location,
            **validated_data
        )
        
        return point
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        
        # Добавляем координаты в ответ
        if instance.location:
            representation['latitude'] = instance.location.y
            representation['longitude'] = instance.location.x
        
        return representation


class MessageSerializer(serializers.ModelSerializer):
    point = serializers.PrimaryKeyRelatedField(
        queryset=Point.objects.all(),
        write_only=True,
        help_text="ID точки, к которой относится сообщение"
    )
    
    # Координаты для сообщения (опционально)
    message_latitude = serializers.FloatField(
        write_only=True,
        required=False,
        allow_null=True,
        help_text="Широта сообщения (если отличается от точки)"
    )
    message_longitude = serializers.FloatField(
        write_only=True,
        required=False,
        allow_null=True,
        help_text="Долгота сообщения (если отличается от точки)"
    )
    
    class Meta:
        model = Message
        fields = '__all__'
    
    def create(self, validated_data):
        # Обрабатываем координаты сообщения, если они предоставлены
        message_latitude = validated_data.pop('latitude', None)
        message_longitude = validated_data.pop('longitude', None)
        
        if message_latitude is not None and message_longitude is not None:
            validated_data['location'] = GeoPoint(
                message_longitude,
                message_latitude,
                srid=4326
            )
        
        return super().create(validated_data)
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        
        # Добавляем координаты сообщения в ответ
        if instance.location:
            representation['latitude'] = instance.location.y
            representation['longitude'] = instance.location.x
        
        return representation


class SearchSerializer(serializers.Serializer):
    latitude = serializers.FloatField(
        required=True,
        help_text="Широта центра поиска"
    )
    longitude = serializers.FloatField(
        required=True,
        help_text="Долгота центра поиска"
    )
    radius = serializers.FloatField(
        required=True,
        min_value=0.1,
        max_value=1000,
        help_text="Радиус поиска в километрах"
    )