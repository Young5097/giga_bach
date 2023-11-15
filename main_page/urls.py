from django.urls import path
from . import views
from .views import login_view, signup_view, find_username_view

urlpatterns = [
    path('', views.main, name='main'),
    path('login/', login_view, name='login'),
    path('signup/', signup_view, name='signup'),
    path('find_username/', find_username_view, name='find_username'),
]
