from django.shortcuts import render


# Create your views here.
def make_song(request):
    return render(request, "make_song.html")
