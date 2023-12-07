from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.conf import settings
from .forms import SongForm
from .sound2to2midi import sound2midi
from .midi_catcher import identify_instruments
import os


def make_song(request):
    if request.method == "POST":
        form = SongForm(request.POST, request.FILES)
        if form.is_valid():
            song = form.save()

            audio_file_path = song.audio_file.path

            # 음악 파일이 MIDI 확장자인지 확인
            if audio_file_path.endswith(".midi") or audio_file_path.endswith(".mid"):
                identify_instruments(audio_file_path)
            else:
                sound2midi(audio_file_path)

            # make_song 페이지로 리다이렉트
            return redirect("ms_result")
    else:
        form = SongForm()

    return render(request, "make_song.html", {"form": form})


def ms_result(request):
    # 세션에서 MIDI 파일의 경로를 가져옴
    midi_file_path = "./APTITUDE/media/got_temp_midi/outputs.mid"

    if midi_file_path:
        return render(request, "ms_result.html", {"midi_file_path": midi_file_path})
    else:
        return HttpResponse("Error: MIDI file not found.")


def download_midi(request):
    # 세션에서 MIDI 파일의 경로를 가져옴
    midi_file_path = "./APTITUDE/media/got_temp_midi/outputs.mid"

    if midi_file_path:
        # MIDI 파일이 존재하면 파일을 읽어서 응답으로 반환
        with open(midi_file_path, "rb") as midi_file:
            response = HttpResponse(midi_file.read(), content_type="audio/midi")
            response[
                "Content-Disposition"
            ] = f"attachment; filename={os.path.basename(midi_file_path)}"
            return response
    else:
        return HttpResponse("Error: MIDI file not found.")

