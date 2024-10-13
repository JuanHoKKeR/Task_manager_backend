# tasks/urls.py

from django.urls import path, include
from rest_framework import routers
from .api import TaskViewSet, UserViewSet, TagViewSet, TaskStaticsView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = routers.DefaultRouter()
router.register(r'tasks', TaskViewSet, basename='task')
router.register(r'users', UserViewSet, basename='user')
router.register(r'tags', TagViewSet, basename='tag')

urlpatterns = [
    path('', include(router.urls)),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('statistics/', TaskStaticsView.as_view(), name='task_statistics')
]
