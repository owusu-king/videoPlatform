from django.shortcuts import render

# Video page, denoting the index view
def index(request): 
    return render(request, 'video/index.html',)
