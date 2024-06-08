from django.shortcuts import render
from .forms import UserCreationForm

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
