from django.urls import path
from . import views

app_name = 'booking'  # Set the app_name here

urlpatterns = [
    path('', views.meal_list),
    path('summernote/', include('django_summernote.urls')),
    path('<slug:slug>' , views.meal_detail , name='meal_detail')
]