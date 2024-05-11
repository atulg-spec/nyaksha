from django.urls import path
from dashboard.views import *
# urls.py
urlpatterns = [
    # PAGES
    path("login",handle_login,name='login'),
    path("dashboard",dashboard,name='dashboard'),
    path("webhook/<str:url>",webhook,name='webhook'),
    path("history",history,name='history'),
    path("portfolio",portfolio,name='portfolio'),
    path("performance",performance,name='performance'),
    path("profile",profile,name='profile'),
    path("plans",plans,name='plans'),
    path("contactus",contactus,name='contactus'),
    # # POLICY
    path("indicator",indicator,name='indicator'),
    path("logout/",handlelogout,name='logout'),
]
