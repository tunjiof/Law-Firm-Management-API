from django.db import models
from clients.models import Client 
from django.contrib.auth import get_user_model

# Create your models here.

User = get_user_model()

class Case(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=50, choices=[
        ('Open', 'Open'),
        ('Closed', 'Closed'),
        ('Pending', 'Pending'),
    ])
    assigned_lawyer = models.ForeignKey(User, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
