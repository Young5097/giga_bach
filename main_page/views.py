from django.shortcuts import render

# Create your views here.
def index(request):
    return render(
        request,
        'main_page/index.html'
    )

def login(request):
    return render(
        request,
        'main_page/login.html'
    )

def register(request):
    return render(
        request,
        'main_page/register.html'
    )