from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import date, timedelta
from .models import Booking
from .forms import ReservationForm

class BookingSystemTestCase(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def create_booking(self, date_str, time='09:00', group=4, status='Pending', guest=None):
        # Create a booking
        return Booking.objects.create(
            guest=guest or self.user,
            date=date_str,
            time=time,
            group=group,
            status=status
        )

        def test_booking_creation(self):
        # Test if a booking can be created
            booking = self.create_booking(date.today() + timedelta(days=1))
            self.assertIsInstance(booking, Booking)

        def test_duplicate_booking_rejected(self):
        # Test that a duplicate booking on the same date and time is rejected
            self.create_booking(date.today() + timedelta(days=1))
            form_data = {'date': date.today() + timedelta(days=1), 'time': '09:00', 'group': 4, 'status': 'Pending'}
            form = ReservationForm(data=form_data)
            self.assertFalse(form.is_valid())

        def test_valid_booking_form(self):
        # Test if the booking form is valid with correct input
            form_data = {'date': date.today() + timedelta(days=2), 'time': '09:30', 'group': 3, 'status': 'Pending'}
            form = ReservationForm(data=form_data)
            self.assertTrue(form.is_valid())

        def test_invalid_group_size_rejected(self):
        # Test that a booking with an invalid group size is rejected
            form_data = {'date': date.today() + timedelta(days=3), 'time': '10:00', 'group': 20, 'status': 'Pending'}
            form = ReservationForm(data=form_data)
            self.assertFalse(form.is_valid())

        def test_booking_list_view(self):
        # Test the booking list view for a logged-in user
            self.client.login(username='testuser', password='testpassword')
            response = self.client.get(reverse('bookinglist'))
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, 'bookinglist.html')
