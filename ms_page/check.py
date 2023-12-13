from getmusic import generate_music, convert_midi_to_wav
from midi2csv import midi_to_csv
import os
import subprocess

directory_path = '/content/drive/MyDrive/giga_bach/ms_page'
os.chdir(directory_path)
command = f'python midi2df2midi.py'
subprocess.run(command, shell=True)
directory_path = '/content/drive/MyDrive/giga_bach'
os.chdir(directory_path)

load_path = "/content/drive/MyDrive/giga_bach/checkpoint.pth"
file_path = "/content/drive/MyDrive/giga_bach/APTITUDE/media/getmusic_result/midi2df2midi"
generate_music(load_path, file_path, 'p', 'b d g', 3)
directory_path = '/content/drive/MyDrive/giga_bach/'
os.chdir(directory_path)
            

