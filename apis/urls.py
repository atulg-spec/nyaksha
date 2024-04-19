from django.urls import path
from .views import *
# urls.py
urlpatterns = [
    path("status/<str:broker>/<str:id>",status,name='status'),
    path("delete/<str:broker>/<str:id>",delete,name='delete'),
    path("angelone",angelone,name='angelone'),
    path("dhanhq",dhanhq,name='dhanhq'),
]
