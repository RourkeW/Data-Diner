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

        def test_booking_delete_view(self):
        # Test the booking delete view for a logged-in user
            booking = self.create_booking(date.today() + timedelta(days=4))
            url = reverse('delete', args=[booking.pk])
            self.client.login(username='testuser', password='testpassword')
            response = self.client.post(url)
            self.assertEqual(response.status_code, 302)  # Redirects to booking list

        def test_custom_404_view(self):
        # Test the custom 404 view
            response = self.client.get('/nonexistentpage/')
            self.assertEqual(response.status_code, 404)
            self.assertTemplateUsed(response, '404.html')

        def test_update_own_booking(self):
        # Test if a user can update their own booking
            booking = self.create_booking(date.today() + timedelta(days=5))
            url = reverse('bookingupdate', args=[booking.pk])
            form_data = {'date': date.today() + timedelta(days=6), 'time': '11:00', 'group': 5, 'status': 'Pending'}
            self.client.login(username='testuser', password='testpassword')
            response = self.client.post(url, data=form_data)
            self.assertEqual(response.status_code, 302)  # Redirects to booking list
            updated_booking = Booking.objects.get(pk=booking.pk)
            self.assertEqual(updated_booking.date, date.today() + timedelta(days=6))
            self.assertEqual(updated_booking.time, '11:00')
            self.assertEqual(updated_booking.group, 5)

        def test_update_other_user_booking(self):
        # Test if a user cannot update another user's booking
            other_user = User.objects.create_user(username='otheruser', password='testpassword')
            booking = self.create_booking(date.today() + timedelta(days=7), group=3, guest=other_user)
            url = reverse('bookingupdate', args=[booking.pk])
            form_data = {'date': date.today() + timedelta(days=8), 'time': '13:30', 'group': 4, 'status': 'Pending'}
            self.client.login(username='testuser', password='testpassword')
            response = self.client.post(url, data=form_data)
            self.assertEqual(response.status_code, 403)  # Forbidden

        def test_delete_own_booking(self):
        # Test if a user can delete their own booking
            booking = self.create_booking(date.today() + timedelta(days=9))
            url = reverse('delete', args=[booking.pk])
            self.client.login(username='testuser', password='testpassword')
            response = self.client.post(url)
            self.assertEqual(response.status_code, 302)  # Redirects to booking list
            with self.assertRaises(Booking.DoesNotExist):
                Booking.objects.get(pk=booking.pk)

        def test_delete_other_user_booking(self):
        # Test if a user cannot delete another user's booking
            other_user = User.objects.create_user(username='otheruser', password='testpassword')
            booking = self.create_booking(date.today() + timedelta(days=10), group=3, guest=other_user)
            url = reverse('delete', args=[booking.pk])
            self.client.login(username='testuser', password='testpassword')
            response = self.client.post(url)
            self.assertEqual(response.status_code, 403)  # Forbidden

        def test_user_authentication(self):
        # Test that only authenticated users can access certain views
            response = self.client.get(reverse('bookform'))
            self.assertEqual(response.status_code, 200)  # Redirects to login page for unauthenticated users

        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('bookform'))
        self.assertEqual(response.status_code, 200)

        def test_user_authorization(self):
        # Test that users cannot update or delete bookings created by other users
            other_user = User.objects.create_user(username='otheruser', password='testpassword')
            other_user_booking = self.create_booking(date.today() + timedelta(days=1), guest=other_user)

        url = reverse('bookingupdate', args=[other_user_booking.pk])
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)  # Forbidden

        url = reverse('delete', args=[other_user_booking.pk])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 403)

        def test_date_time_availability(self):
            booking = self.create_booking(date.today() + timedelta(days=2))

        form_data = {'date': date.today() + timedelta(days=2), 'time': '09:00', 'group': 4, 'status': 'Pending'}
        form = ReservationForm(data=form_data)
        self.assertFalse(form.is_valid())

        def test_error_handling(self):
        # Test error handling scenarios
            response = self.client.get('/nonexistentpage/')
            self.assertEqual(response.status_code, 404)
            self.assertTemplateUsed(response, '404.html')

        form_data = {'date': date.today(), 'time': 'invalid_time', 'group': 20, 'status': 'Pending'}
        form = ReservationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('Select a valid choice. invalid_time is not one of the available choices.', form.errors['time'])
        self.assertIn('Group size must be between 1 and 15', form.errors['group'])
