from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('email','phone_number' ,'first_name', 'is_suscribed', 'is_active', 'is_staff')
    list_filter = ('is_staff', 'is_active')
    readonly_fields = ('suscribed_date','expiry_date')
    search_fields = ('email','phone_number' ,'first_name', 'last_name')
    ordering = ('email',)

    fieldsets = (
        (None, {'fields': ('email','phone_number', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name')}),
        ('Quantiy Settings', {'fields': ('default_quantity', 'crudeoil_quantity','nifty_quantity','bank_nifty_quantity','fin_nifty_quantity','bankex_quantity','sensex_quantity')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Suscription Details', {'fields': ('is_suscribed','plan_type')}),
        ('Important dates', {'fields': ('suscribed_date','expiry_date','last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )

    def formfield_for_dbfield(self, db_field, **kwargs):
        formfield = super().formfield_for_dbfield(db_field, **kwargs)
        return formfield

# Register the CustomUserAdmin
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Webhook)

@admin.register(Response)
class Response(admin.ModelAdmin):
    list_display = ('user','broker','api_name','created_at','response')
    list_filter = ('user', 'created_at','broker')
    search_fields = ('api_name',)


@admin.register(contact_us)
class contact_us(admin.ModelAdmin):
    list_display = ('user','phone_number_or_email','subject','datetime')
    list_filter = ('user','datetime',)
    search_fields = ('user','phone_number_or_email',)

@admin.register(Order)
class Order(admin.ModelAdmin):
    list_display = ('symbol','segment','price','order_type','transaction_type','stoploss','target','created_at')
    list_filter = ('created_at',)
    search_fields = ('symbol','token')

admin.site.register(brokers)
admin.site.register(users)

from social_django.models import Nonce,UserSocialAuth,Association
from social_django.admin import Nonce,UserSocialAuth,Association
admin.site.unregister(Nonce)
admin.site.unregister(UserSocialAuth)
admin.site.unregister(Association)


# ----------Admin Customization------------
admin.site.site_header = "Nyaksha Admin"
admin.site.site_title = "Nyaksha Portfolio Management"
admin.site.index_title = " | Admin"
admin.site.unregister(Group)