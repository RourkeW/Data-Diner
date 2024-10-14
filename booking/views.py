from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.views import generic
from .models import Booking
from .forms import ReservationForm
from django.shortcuts import render
from django.views.generic.edit import UpdateView

# Create your views here.
class BookingList(generic.ListView):
    model = Booking
    template_name = "index.html"
    paginate_by = 6

def menu(request):
    return render(request, 'menu.html')

class BookFormView(generic.CreateView):
    model = Booking
    form_class = ReservationForm
    template_name = 'bookingform.html'
    success_url = reverse_lazy('bookinglist')

    def form_valid(self, form):
        print("Form is valid. Checking for existing bookings...")
        selected_date = form.cleaned_data['date']
        selected_time = form.cleaned_data['time']

        # Check for existing bookings on the selected date and time
        existing_booking = Booking.objects.filter(date=selected_date, time=selected_time).first()

        if existing_booking and existing_booking.status != 'Cancelled':
            messages.error(self.request, 'Booking for the selected date and time already exists.')
            return self.form_invalid(form)

        form.instance.guest = self.request.user
        messages.success(self.request, 'Booking submitted successfully')
        return super().form_valid(form)

    def form_invalid(self, form):
        if 'group' in form.errors:
            messages.error(self.request, 'Group size must be between 1 and 15.')
        else:
            messages.error(self.request, 'Booking for the selected date and time already exists.')
            return super().form_invalid(form)

class BookUpdateView(UserPassesTestMixin, UpdateView):
    model = Booking
    form_class = ReservationForm
    template_name = 'bookingupdate.html'
    success_url = reverse_lazy('bookinglist')

    def test_func(self):
        return self.request.user.id == self.get_object().guest.id

    def form_valid(self, form):
        form.instance.guest = self.request.user
        messages.success(self.request, 'Booking updated successfully')
        return super().form_valid(form)

    def form_invalid(self, form):
        if 'group' in form.errors:
            messages.error(self.request, 'Group size must be between 1 and 15.')
        else:
            messages.error(self.request, 'Booking could not be updated. Please check the details.')
        return super().form_invalid(form)


class BookListView(LoginRequiredMixin, generic.ListView):
    model = Booking
    template_name = 'bookinglist.html'
    paginate_by = 6

    def get_queryset(self):
        return Booking.objects.filter(guest=self.request.user).order_by('date')

class BookDeleteView(UserPassesTestMixin, generic.DeleteView):
    model = Booking
    template_name = 'bookingdelete.html'
    success_url = reverse_lazy('bookinglist')

    def test_func(self):
        return self.request.user.id == self.get_object().guest.id

    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        messages.success(self.request, 'Booking deleted successfully')
        return response
        
    def get_success_url(self):
        messages.success(self.request, 'Booking deleted successfully')
        return reverse_lazy('bookinglist')

def custom_404(request, exception):
    return render(request, '404.html', status=404)