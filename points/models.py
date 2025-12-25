from django.contrib.gis.db import models

class Point(models.Model):
    location = models.PointField(
        verbose_name="Местоположение",
        help_text="Географические координаты точки (широта, долгота)",
        srid=4326,  # WGS84 стандарт
        spatial_index=True,
    )

    def __str__(self):
        return f'{self.location.x:2f} {self.location.y:2f}'
    

class Message(models.Model):
    """
    Модель для сообщений, привязанных к точкам
    """
    point = models.ForeignKey(
        Point,
        on_delete=models.CASCADE,
        help_text="Точка, к которой относится сообщение"
    )
    
    title = models.CharField(
        max_length=255,
        verbose_name="Заголовок сообщения"
    )
    
    content = models.TextField(
        verbose_name="Содержание сообщения",
        help_text="Текст сообщения"
    )

    location = models.PointField(
        verbose_name="Местоположение сообщения",
        help_text="Где было оставлено сообщение",
        srid=4326,
        blank=True,
        null=True,
        spatial_index=True,
    )