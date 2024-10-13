from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from django.contrib.auth.models import User
from .models import Task, Tag
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.files.uploadedfile import SimpleUploadedFile

# Create your tests here.
class UserApiTestCase(APITestCase):
    def test_create_user(self):
        url = reverse('user-list')
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'testpassword'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'newuser')
        self.assertEqual(User.objects.get().email, 'newuser@example.com')

class TaskApiTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password = 'testpassword', email='daviduseche1228@gmail.com')
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
        
    def test_delete_task(self):
        task = Task.objects.create(
            user=self.user,
            title='Test task to delete',
            description='Test description',
            status='pending',
            deadline='2024-12-31'
        )
        url = reverse('task-detail', args=[task.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Task.objects.filter(id=task.id).exists())
        
    def test_update_task(self):
        task = Task.objects.create(
            user=self.user,
            title='Test task to update',
            description='Test description',
            status='pending',
            deadline='2024-12-31'
        )
        url = reverse('task-detail', args=[task.id])
        data = {
            'title': 'Updated title',
            'description': 'Updated description',
            'status': 'completed',
            'deadline': '2024-12-31'
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        task.refresh_from_db()
        self.assertEqual(task.title, 'Updated title')
        self.assertEqual(task.description, 'Updated description')
        self.assertEqual(task.status, 'completed')
        
    def test_create_task_with_attachment(self):
        url = reverse('task-list')
        file = SimpleUploadedFile('file.txt', b'file_content', content_type='text/plain')
        data = {
            'title': 'Test task with attachment',
            'description': 'Test description',
            'status': 'pending',
            'deadline': '2024-12-31',
            'attachment': file
        }
        response = self.client.post(url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('attachment', response.data)
        
    def test_get_statistics(self):
        Task.objects.create(
            user=self.user,
            title='Completed Task',
        description='Description',
        status='completed',
        deadline='2024-12-31'
        )
        Task.objects.create(
            user=self.user,
            title='Pending Task',
            description='Description',
            status='pending',
            deadline='2024-12-31'
        )
        Task.objects.create(
            user=self.user,
            title='Overdue Task',
            description='Description',
            status='pending',
            deadline='2020-01-01'
        )
        url = reverse('task_statistics')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['total_tasks'], 3)
        self.assertEqual(response.data['completed_tasks'], 1)
        self.assertEqual(response.data['pending_tasks'], 2)
        self.assertEqual(response.data['overdue_tasks'], 1)
        
    def test_assign_tags_to_task(self):
        tag1 = Tag.objects.create(user=self.user, name='Personal')
        tag2 = Tag.objects.create(user=self.user, name='Urgente')
        url = reverse('task-list')
        data = {
            'title': 'Compra Viveres',
            'description': 'Comprar viveres para la semana',
            'status': 'pending',
            'deadline': '2024-12-31',
            'tags': [
                {'name': 'Personal'},
                {'name': 'Urgente'}
            ]
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(response.data['tags']), 2)
