"""
URLs mapping for users.
"""
from django.urls import path
from .views import UserMeRetrieveView

app_name = 'user_api'
urlpatterns = [
    path('me/', UserMeRetrieveView.as_view(), name='me')
]
