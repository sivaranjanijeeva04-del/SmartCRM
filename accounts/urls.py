from django.urls import path
from . import views


urlpatterns = [

    # Home
    path(
        '',
        views.login_view,
        name='home'
    ),

    # Authentication
    path(
        'signup/',
        views.signup,
        name='signup'
    ),

    path(
        'login/',
        views.login_view,
        name='login'
    ),

    path(
        'logout/',
        views.logout_view,
        name='logout'
    ),

    # Dashboard
    path(
        'dashboard/',
        views.dashboard,
        name='dashboard'
    ),

    # Profile
    path(
        'profile/',
        views.profile,
        name='profile'
    ),
]