from music21 import converter, note, chord, stream
import csv

def extract_notes_and_chords(music_element, offset):
    result = []
    if 'Chord' in music_element.classes:
        for pitch in music_element.pitches:
            result.append((offset, pitch.ps, music_element.volume.velocity))
    elif 'Note' in music_element.classes:
        result.append((offset, music_element.pitch.ps, music_element.volume.velocity))
    return result

def midi_to_csv(midi_file_path, csv_file):
    # MIDI 파일 불러오기
    midi_stream = converter.parse(midi_file_path)

    # CSV 파일 생성
    with open(csv_file, 'w', newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file)

        # 헤더 작성
        csv_writer.writerow(['Offset', 'Pitch', 'Velocity'])

        # 모든 파트의 음표와 코드를 반복
        for part in midi_stream.parts:
            offset = 0
            for element in part.flat.notesAndRests:
                # 음표와 코드 정보를 추출하여 CSV에 작성
                for note_info in extract_notes_and_chords(element, offset):
                    csv_writer.writerow(note_info)
                offset += element.duration.quarterLength

# if __name__ == "__main__":
#     midi_file_path = '/Users/bongmin/Desktop/gigabach/Game_of_Thrones_Easy_piano.mid'
#     csv_file_path = '/Users/bongmin/Desktop/gigabach/midi.csv'

#     midi_to_csv(midi_file_path, csv_file_path)







