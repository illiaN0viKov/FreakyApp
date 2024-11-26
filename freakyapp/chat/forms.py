from .models import *
from django import forms


class MessageForm(forms.ModelForm):
    class Meta:
        model = GroupMessage
        fields = ["text"]
        widgets = {"text": forms.TextInput(
                attrs={
                    "placeholder": "Add message...", 
                    "class": "w-full h-full rounded-2xl px-4 py-3 border-none outline-none", 
                    "maxlength": "300", 
                    "autofocus": "True",
                }
            ),
                                        }
        