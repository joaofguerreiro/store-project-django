from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.validators import ASCIIUsernameValidator


ERROR_MESSAGES = {
        'username': 'This username is already in use. Please select a different one.',
        'ascii': 'You can only use ASCII characters.',
        'email': 'This email is already in use. Please select a different one.',
    }


class UserForm(forms.ModelForm):
    email = forms.CharField(widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'First Name'}), required=False)
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Last Name'}), required=False)
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username'}), required=True)

    class Meta:
        model = User

        fields = ['first_name', 'last_name', 'username', 'email', 'password']

    def clean_username(self):
        username = self.cleaned_data['username']
        user = User.objects.filter(username=username)
        username_validator = ASCIIUsernameValidator()

        if user.exists():
            raise forms.ValidationError(ERROR_MESSAGES['username'])

        if username_validator:
            raise forms.ValidationError(ERROR_MESSAGES['ascii'])

        return username

