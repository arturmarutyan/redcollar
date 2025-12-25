from django.db import models

class Point(models.Model):
    lat = models.DecimalField(decimal_places=2)
    lon = models.DecimalField(decimal_places=2)

    def __str__(self):
        return f'{self.lat} {self.lon}'
    

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
    
    author = models.CharField(
        max_length=100,
        verbose_name="Автор",
        default="Аноним",
        help_text="Имя или псевдоним автора"
    )
    
    email = models.EmailField(
        verbose_name="Email автора",
        blank=True,
        null=True,
        help_text="Email для обратной связи (необязательно)"
    )
    
    created_at = models.DateTimeField(
        verbose_name="Дата создания",
        auto_now_add=True
    )