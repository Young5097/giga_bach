from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.core.cache import cache
from .forms import SongForm
from .sound2midi import sound2midi
from .midi_catcher import identify_instruments
from .getmusic import generate_music, convert_midi_to_wav
import os
import shutil
import subprocess


def make_song(request):
    if request.method == "POST":
        form = SongForm(request.POST, request.FILES)
        if form.is_valid():
            song = form.save()

            audio_file_path = song.audio_file.path

            request.session.clear()

            # sound2midi ##########################
            if audio_file_path.endswith(".midi") or audio_file_path.endswith(".mid"):
                identify_instruments(audio_file_path)
            else:
                print(audio_file_path)
                sound2midi(audio_file_path)
            ########################################

            # getmusic #############################
            load_path = "/content/drive/MyDrive/giga_bach/checkpoint.pth"

            # 0번째 모델 생성##########
            condition_name = request.POST.getlist("condition")
            content_name = request.POST.getlist("content")
            request.session["condition_name"] = condition_name
            request.session["content_name"] = content_name

            condition_name = " ".join(condition_name)
            content_name = " ".join(content_name)

            file_path = "/content/drive/MyDrive/giga_bach/APTITUDE/media/got_temp_midi"
            generate_music(load_path, file_path, condition_name, content_name, 0)
            directory_path = "/content/drive/MyDrive/giga_bach/"
            os.chdir(directory_path)
            # midi_path = '/content/drive/MyDrive/giga_bach/APTITUDE/media/getmusic_result/midi0/outputs.mid'
            # csv_path = '/content/drive/MyDrive/giga_bach/APTITUDE/media/getmusic_result/midi2csv/midi0.csv'
            # midi_to_csv(midi_path, csv_path)

            # 1번째 모델 생성##########
            file_path = (
                "/content/drive/MyDrive/giga_bach/APTITUDE/media/getmusic_result/midi0"
            )
            generate_music(load_path, file_path, "p", "g", 1)
            directory_path = "/content/drive/MyDrive/giga_bach/"
            os.chdir(directory_path)

            # 2번째 모델 생성##########
            load_path = "/content/drive/MyDrive/giga_bach/checkpoint.pth"
            file_path = (
                "/content/drive/MyDrive/giga_bach/APTITUDE/media/getmusic_result/midi1"
            )
            generate_music(load_path, file_path, "g", "p", 2)
            directory_path = "/content/drive/MyDrive/giga_bach/"
            os.chdir(directory_path)

            # csv 통합 ###############
            directory_path = "/content/drive/MyDrive/giga_bach/ms_page"
            os.chdir(directory_path)
            command = f"python midi2df2midi.py"
            subprocess.run(command, shell=True)
            directory_path = "/content/drive/MyDrive/giga_bach"
            os.chdir(directory_path)

            # 통합된 csv로 getmusic ##
            condition_name = request.POST.getlist("condition")
            content_name = request.POST.getlist("content")
            request.session["condition_name"] = condition_name
            request.session["content_name"] = content_name

            condition_name = " ".join(condition_name)
            content_name = " ".join(content_name)

            file_path = "/content/drive/MyDrive/giga_bach/APTITUDE/media/getmusic_result/midi2df2midi"
            generate_music(load_path, file_path, condition_name, content_name, 3)
            directory_path = "/content/drive/MyDrive/giga_bach/"
            os.chdir(directory_path)
            #######################################

            # midi2wav#######################
            input_folder = (
                "/content/drive/MyDrive/giga_bach/APTITUDE/media/getmusic_result"
            )
            output_folder = "/content/drive/MyDrive/giga_bach/APTITUDE/media/midi2wav"
            convert_midi_to_wav(input_folder, output_folder)
            #################################

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
