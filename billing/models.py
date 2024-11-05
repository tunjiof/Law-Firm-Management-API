from django.conf import settings
from django.db import models
from django.utils import timezone

class Billing(models.Model):
    client = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='billings', on_delete=models.CASCADE)  # Point to custom user model
    # lawyer = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='lawyer_billings', on_delete=models.CASCADE)  # Point to custom user model
    lawyer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='lawyer_billings', null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # Example field for billing amount
    status = models.CharField(max_length=20)  # Example field for billing status
    created_at = models.DateTimeField(default=timezone.now)  # Provide a default value
    updated_at = models.DateTimeField(auto_now=True) # Field for the creation timestamp
    updated_at = models.DateTimeField(auto_now=True)  # Field for the last updated timestamp
    invoice_number = models.CharField(max_length=20, unique=True, null=True)
    def __str__(self):
        return f"Billing {self.id} - {self.client.email}"
