from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from django.contrib.auth.models import User
from .models import Task
from rest_framework_simplejwt.tokens import RefreshToken

# Create your tests here.
class TaskApiTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password = 'testpassword')
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        
    def test_create_task(self):
        url = reverse('task-list')
        data = {
            'title': 'Test task',
            'description': 'Test description',
            'status': 'pending',
            'deadline': '2024-12-31'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
    def test_get_task(self):
        Task.objects.create(
            user=self.user,
            title='Test task',
            description='Test description',
            status='pending',
            deadline='2024-12-31'
        )
        
        url = reverse('task-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)