# accounts/forms.py 中自定義的用戶創建表單

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser ,Reservation, TimeSlot


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'password1', 'password2', '學生', '軍人')


class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['time_slot', 'number_of_people']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['time_slot'].queryset = TimeSlot.objects.filter(available=True)

