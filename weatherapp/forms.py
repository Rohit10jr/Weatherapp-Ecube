from django import forms 
from django.forms import ModelForm, TextInput
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import City
from crispy_forms.helper import FormHelper

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class CityForm(ModelForm):
    class Meta:
        model = City
        fields = ['name']
        widgets = {
            'name': TextInput(attrs={'class': 'search-input', 'placeholder': 'City Name'}),
        }
        labels = {
            'name': False,
        }
        # updates the input class to have the correct Bulma class and placeholder

        # def __init__(self, *args, **kwargs):
        #     super(CityForm, self).__init__(*args, **kwargs)
        #     self.helper = FormHelper()
        #     self.helper.form_show_labels = False

        #     self.fields['name'].widget.attrs.update({'placeholder': 'City name', 'class':'search-input'})