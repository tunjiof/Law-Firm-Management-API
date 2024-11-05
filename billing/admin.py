from django.contrib import admin
from .models import Billing

class BillingAdmin(admin.ModelAdmin):
    list_display = ('id', 'client', 'lawyer', 'amount', 'status', 'created_at', 'updated_at')  # Ensure these fields exist in the Billing model
    list_filter = ('status', 'client', 'lawyer')  # Ensure these fields exist in the Billing model
    search_fields = ('client__email', 'lawyer__email', 'amount')  # Searchable fields
    ordering = ('-created_at',)  # Order by created_at descending

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs  # Admin can see all
        return qs.filter(client=request.user)  # Filter to client entries for non-admin users

admin.site.register(Billing, BillingAdmin)
