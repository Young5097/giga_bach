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
import mimetypes
from .models import Song
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout



def make_song(request):
    if request.method == "POST":
        form = SongForm(request.POST, request.FILES)
        if form.is_valid():
            
            #선택 악기 및 제목과 파일경로 db 저장 #########
            condition_track = request.POST.getlist("condition")
            content_track = request.POST.getlist("content")

            condition_track = "  ".join(condition_track)
            content_track = "  ".join(content_track)
            
            song = form.save(commit=False)
            song.user = request.user
            song.condition_track = condition_track
            song.content_track = content_track
            song.save()

            audio_file_path = song.audio_file.path
            #############################################

            # sound2midi ##########################
            if audio_file_path.endswith(".midi") or audio_file_path.endswith(".mid"):
                identify_instruments(audio_file_path)

                old_path = audio_file_path
                new_path = "/content/drive/MyDrive/giga_bach/APTITUDE/media/got_temp_midi/outputs.mid"
                os.rename(old_path, new_path)
            else:
                sound2midi(audio_file_path)
            ########################################

            # getmusic #############################
            load_path = "/content/drive/MyDrive/giga_bach/checkpoint.pth"

            # 0번째 모델 생성#########
            file_path = "/content/drive/MyDrive/giga_bach/APTITUDE/media/got_temp_midi"
            generate_music(load_path, file_path, condition_track, content_track, 0)
            directory_path = "/content/drive/MyDrive/giga_bach/"
            os.chdir(directory_path)

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

            # df 통합 ###############
            directory_path = "/content/drive/MyDrive/giga_bach/ms_page"
            os.chdir(directory_path)
            command = f"python midi2df2midi.py"
            subprocess.run(command, shell=True)
            directory_path = "/content/drive/MyDrive/giga_bach"
            os.chdir(directory_path)

            # 통합된 df로 getmusic ##
            file_path = "/content/drive/MyDrive/giga_bach/APTITUDE/media/getmusic_result/midi2df2midi"
            generate_music(load_path, file_path, condition_track, content_track, 3)
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

            # 파일 삭제 (덮어쓰기 오류 방지) #######################
            os.remove(
                "/content/drive/MyDrive/giga_bach/APTITUDE/media/got_temp_midi/outputs.mid"
            )
            os.remove(
                "/content/drive/MyDrive/giga_bach/APTITUDE/media/getmusic_result/midi0/outputs.mid"
            )
            os.remove(
                "/content/drive/MyDrive/giga_bach/APTITUDE/media/getmusic_result/midi1/outputs.mid"
            )
            os.remove(
                "/content/drive/MyDrive/giga_bach/APTITUDE/media/getmusic_result/midi2/outputs.mid"
            )
            os.remove(
                "/content/drive/MyDrive/giga_bach/APTITUDE/media/getmusic_result/midi2df2midi/output_mid.mid"
            )
            os.remove(
                "/content/drive/MyDrive/giga_bach/APTITUDE/media/getmusic_result/output_mid.mid"
            )
            ##################################

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


def download_wav(request):
    # 세션에서 MIDI 파일의 경로를 가져옴
    wav_file_path = "./APTITUDE/media/midi2wav/output_mid.wav"

    if wav_file_path:
        # MIDI 파일이 존재하면 파일을 읽어서 응답으로 반환
        with open(wav_file_path, "rb") as midi_file:
            response = HttpResponse(midi_file.read(), content_type="audio/wav")
            response[
                "Content-Disposition"
            ] = f"attachment; filename={os.path.basename(wav_file_path)}"
            return response
    else:
        return HttpResponse("Error: WAV file not found.")


def play_generated_audio(request):
    audio_file_path = (
        "/content/drive/MyDrive/giga_bach/APTITUDE/media/midi2wav/output_mid.wav"
    )

    if os.path.exists(audio_file_path):
        with open(audio_file_path, "rb") as audio_file:
            response = HttpResponse(
                audio_file.read(), content_type=mimetypes.guess_type(audio_file_path)[0]
            )
            response[
                "Content-Disposition"
            ] = f"inline; filename={os.path.basename(audio_file_path)}"
            return response
    else:
        return HttpResponse("Error: Audio file not found.")

def logout_view(request):
    logout(request)
    # 로그아웃 후 리다이렉트할 페이지 지정 (예: 홈페이지)
    return redirect('/')