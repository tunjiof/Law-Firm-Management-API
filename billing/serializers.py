from rest_framework import serializers
from .models import Billing

class BillingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Billing
        fields = ['id', 'client', 'lawyer', 'amount', 'invoice_number', 'created_at', 'updated_at','status']