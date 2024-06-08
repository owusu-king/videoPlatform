from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# A form for Account Creation,
class UserCreationForm(UserCreationForm):
    class Meta:
        model = User
        # Fields needed for registration
        fields = ['username', 'first_name', 'last_name', 'password1','password1']

    # Implementation to modify some of the attributes of the fields to use email authentication instead of username
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].label = 'Email Address'
        self.fields['username'].widget = forms.TextInput(attrs={
            'type': 'email',  # Change input type here
            'class': 'form-control',  # Optional: add any CSS classes here
        })