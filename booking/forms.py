from django import forms
from .models import Booking
import datetime

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ('date', 'time', 'group', 'status')
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'min': (datetime.date.today() + datetime.timedelta(days=1)).strftime('%Y-%m-%d')}),
            'status': forms.HiddenInput(),
        }

        def clean(self):
            cleaned_data = super().clean()
        selected_date = cleaned_data.get('date')
        selected_time = cleaned_data.get('time')
        current_booking = self.instance


        existing_bookings = Booking.objects.filter(date=selected_date, time=selected_time).exclude(pk=current_booking.pk)
        if existing_bookings.exists():
            raise forms.ValidationError("This time slot is not available. Please choose a different date or time.")
        return cleaned_data

        def clean_time(self):
            selected_time = self.cleaned_data['time']
        if selected_time not in [choice[0] for choice in Booking.TIME_CHOICES]:
            raise forms.ValidationError("Select a valid choice for time")

            return selected_time
    def clean_group(self):
        selected_group = self.cleaned_data['group']
        if selected_group < 1 or selected_group > 15:
            raise forms.ValidationError("Group size must be between 1 and 15")
        return selected_group