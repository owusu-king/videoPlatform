from django.shortcuts import render
from .models import VideoDetails
from .forms import UserCreationForm, VideoUploadForm
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout

# ACCOUNT VERIFICATION AND PASSWORD RESET MODULES
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.views import PasswordResetConfirmView
from django.urls import reverse_lazy
from .forms import PasswordResetForm




# AUTHENTICATED USER VIEWS FOR ADMINISTRATOR AND NORMAL USERS

def first_video(request):
    if not request.user.is_authenticated: # Non logged in users to be denied access to the video page
        return HttpResponseRedirect(reverse('login'))
    else:
        if request.user.groups.filter(name='Controller').exists():
            return HttpResponseRedirect(reverse('dashboard'))
    first_video = VideoDetails.objects.order_by('pk').first()
    if first_video:
        return HttpResponseRedirect(reverse('index', args=[first_video.pk]))
    else:
        return render(request, 'video/no_video.html')   

# Video page, denoting the index view
def index(request, id): # Pass a video id to display a particular video
    if not request.user.is_authenticated: # Non logged in users to be denied access to the video page
        return HttpResponseRedirect(reverse('login'))
    else:
        if request.user.groups.filter(name='Controller').exists():
            return HttpResponseRedirect(reverse('dashboard'))
    video = VideoDetails.objects.get(id=id)

    next_video = VideoDetails.objects.filter(pk__gt=video.pk).order_by('pk').first()
    previous_video = VideoDetails.objects.filter(pk__lt=video.pk).order_by('-pk').first()

    return render(request, 'video/index.html', {'video' : video, 'next': next_video, 'prev': previous_video}) # Otherwise, give them the index page.

# Dashboard view for Admin to upload videos
def dashboard_view(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))
    else:
        if not request.user.groups.filter(name='Controller').exists():
            if VideoDetails.objects.first():
                return HttpResponseRedirect(reverse('index', args=[VideoDetails.objects.first().id]))
            else:
                return HttpResponseRedirect(reverse('first'))  
        if request.method == 'POST': # If admin uploads a new video
            form = VideoUploadForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
            else:
                return render(request, 'video/dashboard.html', {'video_form': form})        
    return render(request, 'video/dashboard.html', {'video_form': VideoUploadForm()})




# ACCOUNT CREATION, ACTIVATION, LOGIN AND LOGOUT VIEWS
# Signup View, for user registration.
def signup_view(request): 
    if request.user.is_authenticated: # If users are already authenticated, deny this page
        if VideoDetails.objects.first():
            return HttpResponseRedirect(reverse('index', args=[VideoDetails.objects.first().id]))
        else:
            return HttpResponseRedirect(reverse('first'))  
    if request.method == 'POST':
        # when the request method of this view is a POST, then get the form object and save the fields to the db
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False) # Do not commit user details to db yes, lets wait for activation
            user.is_active = False # Set user inactive and save the record
            form.save()

            # do verification
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            current_site = get_current_site(request)
            mail_subject = 'Confirm Account Activation'
            message = render_to_string('video/verification/activate_email_info.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': uid,
                'token': token,
            })
            send_mail(mail_subject, message, settings.EMAIL_HOST_USER, [user.username])
            return render(request, 'video/verification/verification_confirm.html')

            # logout(request) # Stop taking users to the video page after signup,
            # return HttpResponseRedirect(reverse('login')) # Take them to login rather
        else:
            return render(request, 'video/signup.html', {'signup':form}) # if form has errors, then show the errors with the form again  
    return render(request, 'video/signup.html', {'signup':UserCreationForm()}) # if request method is GET, provide a new sign up form

# Activation View,
def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))  # 
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return render(request, 'video/verification/activation_complete.html')
    else:
        return render(request, 'video/verification/activation_invalid.html')


# Login View, for user login action
def login_view(request):
    if request.user.is_authenticated: # If users are already authenticated, deny this page
        if VideoDetails.objects.first():
            return HttpResponseRedirect(reverse('index', args=[VideoDetails.objects.first().id]))
        else:
            return HttpResponseRedirect(reverse('first'))

    if request.method == 'POST':
        # if the request method is POST, get the form fields and authenticate the user
        username = request.POST['username']
        password = request.POST['password']        
        user = authenticate(request, username=username, password = password) # authenticate with django's default authenticate module
        if user is not None:
            login(request, user)
            if VideoDetails.objects.first():
                return HttpResponseRedirect(reverse('index', args=[VideoDetails.objects.first().id]))
            else:
                return HttpResponseRedirect(reverse('first'))
        else:
            return render(request, 'video/login.html', {'message':"Invalid Credentials"}) # If authentication, fails, display login page again, with error message

    return render(request, 'video/login.html') # Defaut request method is GET, so, provide a new login form

# Logout view, destroy user session and take them to the login page
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('login'))




# PASSWORD RESET VIEWS
# A view to request password reset, contains a form for user's email
def password_reset_request(request):
    if request.user.is_authenticated: # If users are already authenticated, deny this page
        if VideoDetails.objects.first():
            return HttpResponseRedirect(reverse('index', args=[VideoDetails.objects.first().id]))
        else:
            return HttpResponseRedirect(reverse('first'))
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            # Get some important details to send an email to the user for reset
            username = form.cleaned_data['username'] 
            user = User.objects.get(username=username)
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            current_site = get_current_site(request)
            mail_subject = 'Password Reset Requested'
            message = render_to_string('video/reset_password/password_reset_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': uid,
                'token': token,
            })
            send_mail(mail_subject, message, settings.EMAIL_HOST_USER, [user.username])
            return HttpResponseRedirect(reverse('password_reset_done'))
    else:
        form = PasswordResetForm()
    return render(request, 'video/reset_password/password_reset_form.html', {'form': form})


# confirm
class PasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'video/reset_password/password_reset_confirm.html'
    success_url = reverse_lazy('password_reset_complete')

    def dispatch(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse('first'))  # Ensure authenticated users cannot access this view
        return super().dispatch(*args, **kwargs)

    
def password_reset_done(request):
    if request.user.is_authenticated: # If users are already authenticated, deny this page
        if VideoDetails.objects.first():
            return HttpResponseRedirect(reverse('index', args=[VideoDetails.objects.first().id]))
        else:
            return HttpResponseRedirect(reverse('first'))
    return render(request, 'video/reset_password/password_reset_done.html')

def password_reset_complete(request):
    if request.user.is_authenticated: # If users are already authenticated, deny this page
        if VideoDetails.objects.first():
            return HttpResponseRedirect(reverse('index', args=[VideoDetails.objects.first().id]))
        else:
            return HttpResponseRedirect(reverse('first'))
    return render(request, 'video/reset_password/password_reset_complete.html')