from django.contrib import admin
from .models import *
# Register your models here.

@admin.register(angel_api)
class angel_api(admin.ModelAdmin):
    list_display = ('user','api_name','created_time','api_key','client_id','is_trading')
    list_filter = ('user', 'created_time','is_trading')


@admin.register(dhan_api)
class dhan_api(admin.ModelAdmin):
    list_display = ('user','api_name','created_time','client_id','is_trading')
    list_filter = ('user', 'created_time','is_trading')