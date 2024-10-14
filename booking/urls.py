from . import views
from django.urls import path

handler404 = 'booking.views.custom_404'

urlpatterns = [
    path('', views.BookingList.as_view(), name='home'),
    path('menu/', views.menu, name='menu'),
    path('bookinglist/', views.BookListView.as_view(), name='bookinglist'),
    path('<pk>/delete/', views.BookDeleteView.as_view(), name='delete'),
    path('<pk>/update/', views.BookUpdateView.as_view(), name='bookingupdate'),
    path('bookform/', views.BookFormView.as_view(), name='bookform'),
    path('custom_404/', views.custom_404, name='custom_404'),
]