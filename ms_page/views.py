from django.shortcuts import render, redirect
from .forms import UploadAudioForm


# Create your views here.
def make_song(request):
    if request.method == "POST":
        form = UploadAudioForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("sucess_song")
    else:
        form = UploadAudioForm()
    return render(request, "make_song.html", {"form": form})


def sucess_song(request):
    return render(request, "sucess_song.html")
