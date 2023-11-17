from django.shortcuts import render


# Create your views here.
def make_vocal(request):
    return render(request, "make_vocal.html")
