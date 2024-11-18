from .models import Event, Topic
from django import forms
from datetime import date
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'date', 'maxPeople']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'min': date.today().strftime('%Y-%m-%d')}),  
            'maxPeople': forms.NumberInput(attrs={'min': '1', 'step': '1', })
        }

class TopicForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['topics']
    topics = forms.ModelMultipleChoiceField(
        queryset=Topic.objects.all(),  # Provide the queryset for the available topics
        widget=forms.CheckboxSelectMultiple,  # Use CheckboxSelectMultiple widget
        required=True,  # Set required to False if it's optional
        label="Select Event Topics"
    )


class RegForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


        