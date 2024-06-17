from django.shortcuts import render
import os
from .models import Video
from .forms import UserCreationForm, VideoUploadForm
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout

# ACCOUNT VERIFICATION AND PASSWORD RESET MODULES
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.views import PasswordResetConfirmView
from django.urls import reverse_lazy
from .forms import PasswordResetForm
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .forms import ShareLinkForm
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
from django.db.models import F, Value, CharField
from django.db.models.functions import Substr, Concat



# VIDEO PAGE, AND THE ADMIN DASHBOARD VIEWS

# Check if there is a video in the database so that the index page wouldn't return error.
def first_video(request):
    # redirect non authenticated users to login
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))
    else:
        # Redirect administrators to dashboard
        if request.user.groups.filter(name='Controller').exists():
            return HttpResponseRedirect(reverse('dashboard'))
    first_video = Video.objects.order_by('pk').first()
    # Go to the index page if there is a video in the database.
    if first_video:
        return HttpResponseRedirect(reverse('index', args=[first_video.pk]))
    else:
        # If the database is empty, then render a NO video page.
        return render(request, 'video/no_video.html')  

# Home page, where non administrative users will watch videos
def index(request, id): # Pass a video id to display a particular video
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))
    else:
        if request.user.groups.filter(name='Controller').exists():
            return HttpResponseRedirect(reverse('dashboard'))
    # Get the video object by id, passed to this view
    video = Video.objects.get(id=id)
    # Find next and previous objects in the database.
    next_video = Video.objects.filter(pk__gt=video.pk).order_by('pk').first()
    previous_video = Video.objects.filter(pk__lt=video.pk).order_by('-pk').first()
    # Render the index page with the video object, next and previous video objects.
    return render(request, 'video/index.html', 
                  {'video' : video, 'next': next_video, 'prev': previous_video})

# Dashboard where administrative users can upload videos and 
def dashboard_view(request):
    # Get all videos to display few logs. also, to make the logs clean, get only 40 chars out of the title and append ...
    videos = Video.objects.annotate(
    truncated_title=Substr(F('title'), 1, 40, output_field=CharField())).annotate(display_title=Concat(F('truncated_title'), 
    Value('...'), output_field=CharField())).order_by('-pk')[:7]
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))
    else:
        # Take users to video page if they are not administrators
        if not request.user.groups.filter(name='Controller').exists():
            return HttpResponseRedirect(reverse('first'))
        # Handle  POST request for video upload  
        if request.method == 'POST': # If admin uploads a new video
            form = VideoUploadForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
            else:
                return render(request, 'video/dashboard.html', {'video_form': form}) # Give back the forms with errors if there is      
    return render(request, 'video/dashboard.html', {'video_form': VideoUploadForm(), 'logs': videos})



# ACCOUNT CREATION, ACTIVATION, LOGIN AND LOGOUT VIEWS

# Signup View, for user registration.
def signup_view(request): 
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('first'))   
    # Handle post request for account creation
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # Save information and set user inactive to validate verification
            user = form.save(commit=False)
            user.is_active = False
            form.save()            
            # Generate token for account verification via email
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            current_site = get_current_site(request)
            mail_subject = 'Confirm Account Activation'
            context = {
                'user': user,
                'domain': current_site.domain,
                'uid': uid,
                'token': token,
                'protocol': 'http',
            }
            html_content = render_to_string('video/verification/activate_email_info.html', context )
            text_content = strip_tags(html_content)
            # Sent a well formatted verification email.
            msg = EmailMultiAlternatives(mail_subject, text_content, settings.EMAIL_HOST_USER, [user.username])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            return render(request, 'video/verification/verification_confirm.html')
        else:
            return render(request, 'video/signup.html', {'signup':form})
    # Render a new form for initial request (GET) 
    return render(request, 'video/signup.html', {'signup':UserCreationForm()}) 

# Activation View,
def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))  # 
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
        return HttpResponseRedirect(reverse('login'))   
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return render(request, 'video/verification/activation_complete.html')    
    elif user.is_active == True and not default_token_generator.check_token(user, token):
        return render(request, 'video/verification/already_verified.html')
    else:
        if user.is_active == False and not default_token_generator.check_token(user, token):
            user.delete()
            return render(request, 'video/verification/activation_invalid.html')

# Login View,
message = '' # set appropriate error message for failed authentication
def login_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('first'))
    if request.method == 'POST':
        # if the request method is POST, get the form fields and authenticate the user.
        username = request.POST['username']
        password = request.POST['password']        
        user = authenticate(request, username=username, password = password)        
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('first'))
        else:
            if User.objects.filter(username=username).exists():
                message = "Incorrect password, try again"
            else:
                message = "No user with this email exist."
            # If authentication, fails, return the login page, with an error message
            return render(request, 'video/login.html', {'message':message}) 
    # Defaut request method is GET, so, provide a new login form
    return render(request, 'video/login.html') 

# Logout view, destroy user session and take them to the login page
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('login'))



# BASIC VIDEO ACTIONS ADD ON THE DASHBOARD

# Edit Video by Administrator
def edit_video(request, id):
    if not request.user.is_authenticated: # Non logged in users to be denied access to the video page
        return HttpResponseRedirect(reverse('login'))
    else:
        if not request.user.groups.filter(name='Controller').exists():
            return HttpResponseRedirect(reverse('first'))
    # Get the particular video which called the edit view and show it's instance for edit
    video = Video.objects.get(pk=id)
    if request.method =='POST':
        form = VideoUploadForm(request.POST, instance=video)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('dashboard'))
    # Render a new edit page when request is GET
    return render(request, 'video/edit.html', {'form':VideoUploadForm(instance=video)})

# Delete the View
def delete_video(request, id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))
    elif not request.user.groups.filter(name='Controller').exists():
        return HttpResponseRedirect(reverse('first'))   
    try:
        video = Video.objects.get(pk=id)
    except Video.DoesNotExist:
        return HttpResponseRedirect(reverse('dashboard'))
    # Get the file path and construct the absolute path
    file_path = os.path.join(settings.MEDIA_ROOT, str(video.video_file))
    # Delete the file from disk if it exists
    if os.path.exists(file_path):
        os.remove(file_path)
    # Delete the Video object from the database
    video.delete()
    return HttpResponseRedirect(reverse('dashboard'))



# PASSWORD RESET VIEWS

# A view to request password reset, contains a form for user's email
def password_reset_request(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('first'))
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            # Get some important details to send a reset link email to the user
            username = form.cleaned_data['username'] 
            user = User.objects.get(username=username)
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            current_site = get_current_site(request)
            mail_subject = 'Password Reset Requested'
            context =  {
                'user': user,
                'domain': current_site.domain,
                'uid': uid,
                'token': token,
                'protocol': 'http',
            }
            html_content = render_to_string('video/reset_password/password_reset_email.html', context )
            text_content = strip_tags(html_content)
            msg = EmailMultiAlternatives(mail_subject, text_content, settings.EMAIL_HOST_USER, [user.username])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            return HttpResponseRedirect(reverse('password_reset_done'))
    else:
        form = PasswordResetForm()
    return render(request, 'video/reset_password/password_reset_form.html', {'form': form})

# confirm by setting a new password
class PasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'video/reset_password/password_reset_confirm.html'
    success_url = reverse_lazy('password_reset_complete')

# A view to show reset request is sent to mail   
def password_reset_done(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('first'))
    return render(request, 'video/reset_password/password_reset_done.html')

# A view after new password is set
def password_reset_complete(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('first'))
    return render(request, 'video/reset_password/password_reset_complete.html')

# Ensure only POST request can trigger this method.
@require_POST 
def share_link(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))
    form = ShareLinkForm(request.POST)
    if form.is_valid():
        # Get request details and use the information to send the reset link
        recipient_email = form.cleaned_data['recipient_email']
        message = form.cleaned_data['message']
        page_url = request.POST.get('page_url')  # Get the page URL from the form data
        subject = 'Check out this page'
        message = f"\n{message}\n\n"
        from_email = request.user.username
        rec_uname = recipient_email[:recipient_email.index('@')]
        context = {
            'page_url': page_url,
            'message': message,
            'name': rec_uname,
        }
        try:
            # Try HTML styled format email
            html_content = render_to_string('video/share_email.html', context )
            text_content = strip_tags(html_content)
            msg = EmailMultiAlternatives(subject, text_content, from_email, [recipient_email])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            return JsonResponse({'success': True, 'message': 'Link successfully shared!'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'Error sending email: {e}'})
    else: # If form is not valid, Just an alert of invalid data.
        return JsonResponse({'success': False, 'message': 'Invalid form data'})

