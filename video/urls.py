from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.index, name='index'),
    path('signup/', views.signup_view, name='signup'),

]