from django.urls import path
from . import views

app_name = 'booking'  # Set the app_name here

urlpatterns = [
    path('', views.meal_list),
]