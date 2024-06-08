from django.shortcuts import render
from .forms import UserCreationForm
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout


# Video page, denoting the index view
def index(request): 
    return render(request, 'video/index.html',)



# ACCOUNT CREATION, LOGIN AND LOGOUT VIEWS
# Signup View, for user registration.
def signup_view(request): 
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
    if request.method == 'POST':
        # if the request method is POST, get the form fields and authenticate the user
        username = request.POST['username']
        password = request.POST['password']        
        user = authenticate(request, username=username, password = password) # authenticate with django's default authenticate module
        if user is not None:
            login(request, user)
        else:
            return render(request, 'video/login.html', {'message':"Invalid Credentials"}) # If authentication, fails, display login page again, with error message

    return render(request, 'video/login.html') # Defaut request method is GET, so, provide a new login form


# Logout view, destroy user session and take them to the login page
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('login'))