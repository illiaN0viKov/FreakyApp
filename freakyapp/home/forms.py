from .models import Event
from django import forms
from datetime import date

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'date', 'maxPeople']
        widgets = {
            'date': forms.DateInput(attrs={
                'type': 'date',
                'min': date.today().strftime('%Y-%m-%d')}),  
                'maxPeople': forms.NumberInput(attrs={
                'min': '1', 
                'step': '1', 
            })
                
        }