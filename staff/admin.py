from django.contrib import admin
from .models import Sales

@admin.register(Sales)
class SalesAdmin(admin.ModelAdmin):
    list_display = ['customer_name', 'phone_number', 'user', 'datetime']
    fields = ['customer_name', 'phone_number', 'description']  # Specify fields to display/edit in the admin

    def save_model(self, request, obj, form, change):
        """Override save_model to set the user field based on the current logged-in user."""
        if not obj.user:
            obj.user = request.user  # Set the user to the currently logged-in user if not set
        obj.save()
