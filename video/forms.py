from django import forms
from .models import Video
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# User account creation form,
class UserCreationForm(UserCreationForm):
    # terms and conditions check field
    tnc = forms.BooleanField(
        required = True,
        label='',
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        error_messages={'required': 'Please accept the terms and conditions.'}
    )
    class Meta:
        # Create a form that saves data to the auth user model
        model = User
        # Fields needed for registration
        fields = ['username', 'first_name', 'last_name', 'password1','password2', 'tnc']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].label = 'Email Address'
        self.fields['username'].widget = forms.TextInput(attrs={
            'type': 'email',  # Change input type here
            'class': 'form-control',  # Add any CSS class to style the form
        })

# Video Upload form
class VideoUploadForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['title', 'description', 'video_file']

# Password reset form
class PasswordResetForm(forms.Form):
    username = forms.EmailField(max_length=100, label="Email")
    def clean_username(self):
        username = self.cleaned_data.get('username')
        # Handle non-registered users so I don't end up sending email to generic accounts
        if not User.objects.filter(username=username).exists():
            raise forms.ValidationError("There is no user registered with the specified Email.")
        return username
    
# Share Video Link form
class ShareLinkForm(forms.Form):
    recipient_email = forms.EmailField(label='Recipient Email')
    message = forms.CharField(widget=forms.Textarea, required=False, label='Message')
