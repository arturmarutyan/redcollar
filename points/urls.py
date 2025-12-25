from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PointViewSet, MessageViewSet

router = DefaultRouter()
router.register(r'points', PointViewSet, basename='points')

urlpatterns = [
    path('', include(router.urls)),
    path('points/messages/', 
         MessageViewSet.as_view({
             'get': 'retrieve',
             'put': 'update',
         }), 
         name='message-detail'),
]