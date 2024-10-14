from django.contrib import admin
from django.contrib import messages
from .models import Booking
from django_summernote.admin import SummernoteModelAdmin

class BookingAdmin(SummernoteModelAdmin):
    list_display = ('user', 'date', 'time', 'guests', 'status')
    search_fields = ['user__username', 'user__email']
    list_filter = ('status',)
    date_hierarchy = 'date'

admin.site.register(Booking)
