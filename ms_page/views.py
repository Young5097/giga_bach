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
    # 성공 페이지에서 필요한 데이터를 새로 불러올 수 있습니다.
    return render(request, "sucess_song.html")
