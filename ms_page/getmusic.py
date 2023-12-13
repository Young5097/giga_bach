import os
import miditoolkit
from pydub import AudioSegment
import librosa
import librosa.display
from midi2audio import FluidSynth
from IPython.display import Audio, display
import subprocess


def generate_music(load_path, file_path, main_inst, inst_list, number):
    directory_path = "/content/drive/MyDrive/giga_bach/getmusic"
    os.chdir(directory_path)
    command = f"python track_generation.py --load_path {load_path} --file_path {file_path} --main_inst {main_inst} --inst_list {inst_list} --number {number}"
    subprocess.run(command, shell=True)


def convert_midi_to_wav(input_folder, output_folder):
    fs = FluidSynth()

    for filename in os.listdir(input_folder):
        if filename.endswith(".midi") or filename.endswith(".mid"):
            midi_path = os.path.join(input_folder, filename)
            wav_path = os.path.join(
                output_folder, os.path.splitext(filename)[0] + ".wav"
            )
            fs.midi_to_audio(midi_path, wav_path)

    print("모든 미디 파일을 WAV 파일로 변환하였습니다.")


def play_audio_files(audio_folder):
    supported_formats = [".wav", ".mp3", ".ogg", ".flac"]

    for filename in os.listdir(audio_folder):
        if any(filename.endswith(format) for format in supported_formats):
            file_path = os.path.join(audio_folder, filename)
            display(Audio(file_path, autoplay=True))


# generate_music('/content/drive/MyDrive/giga_bach/checkpoint.pth', '/content/drive/MyDrive/giga_bach/APTITUDE/media/got_temp_midi', 'p', 'b d g')
# convert_midi_to_wav('/content/drive/MyDrive/giga_bach/APTITUDE/media/getmusic_result', '/content/drive/MyDrive/giga_bach/APTITUDE/media/midi2wav')
# play_audio_files('/content/drive/MyDrive/giga_bach/APTITUDE/media/midi2wav')
