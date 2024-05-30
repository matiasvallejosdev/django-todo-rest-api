from django.urls import path
from .views import AutocompleteTaskView

app_name = "ai_api"
urlpatterns = [
    path("autocomplete/", AutocompleteTaskView.as_view(), name="autocomplete"),
]
