from django import forms
from .models import Profile


class UserIDLoginForm(forms.Form):
    user_id = forms.IntegerField(required=True)


class RegistrationForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['user_id']
