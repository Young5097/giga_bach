from django.urls import path
from . import views
from .views import (
    login_view,
    signup_view,
    find_username_view,
    mypage_view,
    edit_profile,
    delete_account,
)
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path("", views.main, name="main"),
    path("login/", login_view, name="login"),
    path("signup/", signup_view, name="signup"),
    path("find_username/", find_username_view, name="find_username"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("mypage/", mypage_view, name="mypage"),
    path("edit_profile/", edit_profile, name="edit_profile"),
    path("delete_account/", delete_account, name="delete_account"),
]
