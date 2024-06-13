from django.urls import path
from . import views


# urls pointing to the individual views in views.py
urlpatterns = [
    path('', views.first_video, name='first'),
    path('home/', views.login_view, name='index'),
    path('home/<int:id>/', views.index, name='index'),
    path('dashboard/', views.dashboard_view, name="dashboard"),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Account verification view
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),

    # Password Reset Views
    path('password_reset/', views.password_reset_request, name='password_reset'),
    path('password_reset/done/', views.password_reset_done, name='password_reset_done'),
    path('reset/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', views.password_reset_complete, name='password_reset_complete'),

    # Setting optional urls to avoid ending slash requirement
    path('home', views.login_view, name='index'),
    path('home/<int:id>', views.index, name='index'),

    path('share-link/', views.share_link, name='share_link'),

    path('delete_video/<int:id>', views.delete_video, name='delete_video')

    #delete
   ]