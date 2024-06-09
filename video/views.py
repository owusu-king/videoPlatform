from django.shortcuts import render
from .forms import UserCreationForm, VideoUploadForm
from django.urls import reverse
from .models import VideoDetails
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
from django.urls import reverse_lazy

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



# ACCOUNT CREATION, LOGIN AND LOGOUT VIEWS
# Signup View, for user registration.
def signup_view(request):
    if request.user.is_authenticated: # If users are already authenticated, deny this page
        return HttpResponseRedirect(reverse('index'))
    if request.method == 'POST':
        # when the request method of this view is a POST, then get the form object and save the fields to the db
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
        else:
            return render(request, 'video/signup.html', {'signup':form}) # if form has errors, then show the errors with the form again  
    return render(request, 'video/signup.html', {'signup':UserCreationForm()}) # if request method is GET, provide a new sign up form


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