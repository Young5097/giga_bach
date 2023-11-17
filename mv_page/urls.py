from django.urls import path
from . import views
from .views import make_vocal

urlpatterns = [
    path("make_vocal/", make_vocal, name="make_vocal"),
]
