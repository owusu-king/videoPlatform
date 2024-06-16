from django import forms
from .models import Video
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# A form for Account Creation,
class UserCreationForm(UserCreationForm):
    tnc = forms.BooleanField(
        required = True,
        label='',
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        error_messages={'required': 'Please accept the terms and conditions.'}
    )


    class Meta:
        model = User
        # Fields needed for registration
        fields = ['username', 'first_name', 'last_name', 'password1','password2', 'tnc']

    # Implementation to modify some of the attributes of the fields to use email authentication instead of username
    def clean_tnc(self):
        tnc = self.cleaned_data.get('tnc')
        if not tnc:
            raise forms.ValidationError('You must agree to the terms and conditions to register.')
        return tnc
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].label = 'Email Address'
        self.fields['username'].widget = forms.TextInput(attrs={
            'type': 'email',  # Change input type here
            'class': 'form-control',  # Optional: add any CSS classes here
        })


# A form for the controller user to upload video
class VideoUploadForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['title', 'description', 'video_file']

        


# password reset form

class PasswordResetForm(forms.Form):
    username = forms.EmailField(max_length=150, label="Email")

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not User.objects.filter(username=username).exists():
            raise forms.ValidationError("There is no user registered with the specified Email.")
        return username

class ShareLinkForm(forms.Form):
    recipient_email = forms.EmailField(label='Recipient Email')
    message = forms.CharField(widget=forms.Textarea, required=False, label='Message')
