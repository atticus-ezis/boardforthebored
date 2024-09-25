from django.urls import path, include
from .views import profile_view

urlpatterns = [
    path('accounts/', include('allauth.urls')),
    path('profile/', profile_view)
]