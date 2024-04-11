from django.urls import path
from dashboard.views import *
# urls.py
urlpatterns = [
    # PAGES
    path("",handle_login,name='login'),
    path("dashboard",dashboard,name='dashboard'),
    path("webhook/<str:url>",webhook,name='webhook'),
    path("history",history,name='history'),
    path("portfolio",portfolio,name='portfolio'),
    path("performance",performance,name='performance'),
    path("profile",profile,name='profile'),
    path("plans",plans,name='plans'),
    path("contactus",contactus,name='contactus'),
    # path("about",about,name='about'),
    # path("disclaimer",disclaimer,name='disclaimer'),
    # path("contactus",contact,name='contactus'),
    # path("pricing",pricing,name='pricing'),
    # # POLICY
    # path("termsofuse",termsofuse,name='termsofuse'),
    # path("disclaimer",disclaimer,name='disclaimer'),
    # path("privacypolicy",privacypolicy,name='privacypolicy'),
    # path("refundpolicy",refundpolicy,name='refundpolicy'),
]
