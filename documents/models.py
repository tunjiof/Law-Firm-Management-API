from django.db import models
from django.conf import settings

# Create your models here.

class Document(models.Model):
    case = models.ForeignKey('cases.Case', related_name='documents', on_delete=models.CASCADE)
    file_name = models.CharField(max_length=255)
    file_type = models.CharField(max_length=50)
    uploaded_date = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to='documents/')

    def __str__(self):
        return self.file_name
