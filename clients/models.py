from django.db import models

# Create your models here.

class Client(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    address = models.TextField()
    case_history = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
