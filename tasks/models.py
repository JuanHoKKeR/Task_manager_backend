from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Tag(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tags')
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name

class Task(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pendiente'),
        ('completed', 'Completada'),
        ('abandoned', 'Abandonada'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    deadline = models.DateField()
    created_at = models.DateField(auto_now_add=True)
    attachment = models.FileField(upload_to='attachments/', null=True, blank=True)
    tags = models.ManyToManyField(Tag, related_name='tasks', blank=True)
    
    def __str__(self):
        return self.title

