from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone
from .models import Task
from django.contrib.auth.models import User
from django.conf import settings

@shared_task
def send_deadline_notifications():
    today = timezone.now().date()
    upcoming_deadline = today + timezone.timedelta(days=1)
    tasks = Task.objects.filter(deadline=upcoming_deadline, status='pending')
    print("Notificaciones de deadline enviadas")
    
    for task in tasks:
        user = task.user
        subject = f"Recordatorio: La tarea '{task.title}' esta proxima a vencer"
        message = f"Hola {user.username},\n\nTu tarea '{task.title}' vence el {task.deadline}. \n\n!No olvides completarla a tiempo!\n\nSaludos,\tTask Manager"
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [user.email]
        send_mail(subject, message, from_email, recipient_list)
