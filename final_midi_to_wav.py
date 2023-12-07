
from pydub import AudioSegment
import librosa
import librosa.display
import os
from midi2audio import FluidSynth
import numpy as np
import pandas as pd
from music21 import converter, note, stream, environment
from midi2audio import FluidSynth
from midiutil import MIDIFile


# FluidSynth을 초기화합니다.
fs = FluidSynth()

# 입력 폴더와 출력 폴더를 설정합니다.
input_folder = '/Users/bongmin/Desktop/giga_bach/music_files' # 추후 final_midi 폴더로 경로 변경
output_folder = '/Users/bongmin/Desktop/giga_bach/get_output_music' # complet_wav 폴더로 경로 변경

# 출력 폴더가 없으면 생성합니다.
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# 입력 폴더 내의 모든 미디 파일에 대해 처리합니다.
for filename in os.listdir(input_folder):
    if filename.endswith(".midi") or filename.endswith(".mid"):
        # MIDI 파일을 WAV 파일로 변환합니다.
        midi_path = os.path.join(input_folder, filename)
        wav_path = os.path.join(output_folder, os.path.splitext(filename)[0] + ".wav")

        # MIDI 파일을 FluidSynth을 사용하여 WAV 파일로 변환합니다.
        fs.midi_to_audio(midi_path, wav_path)

# 변환 완료 메시지를 출력합니다.
print("모든 미디 파일을 WAV 파일로 변환하였습니다.")