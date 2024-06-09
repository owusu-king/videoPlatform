from django.urls import path
from . import views

urlpatterns = [
    path('', views.first_video, name='first'),
    path('home/', views.index, name='index'),
    path('home/<int:id>/', views.index, name='index'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name="dashboard"),

    # Account verification view
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),

]