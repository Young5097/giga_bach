from music21 import converter, stream, note, meter, tempo, instrument
import pandas as pd
import os

def extract_notes_and_chords(music_element, offset):
    result = []
    if 'Chord' in music_element.classes:
        for pitch in music_element.pitches:
            result.append((offset, pitch.ps, music_element.volume.velocity))
    elif 'Note' in music_element.classes:
        result.append((offset, music_element.pitch.ps, music_element.volume.velocity))
    return result

def extract_piano_notes(part):
    data = {'Offset': [], 'Pitch': [], 'Velocity': []}
    offset = 0

    for element in part.flat.notesAndRests:
        for note_info in extract_notes_and_chords(element, offset):
            data['Offset'].append(note_info[0])
            data['Pitch'].append(note_info[1])
            data['Velocity'].append(note_info[2])
        offset += element.duration.quarterLength

    return pd.DataFrame(data)

def midi_to_dataframe(midi_file_path):
    # MIDI 파일 불러오기
    midi_stream = converter.parse(midi_file_path)

    # 피아노 파트만 선택
    piano_part = None
    for part in midi_stream.parts:
        if 'Piano' in part.partName:
            piano_part = part
            break

    if piano_part is not None:
        return extract_piano_notes(piano_part)
    else:
        return pd.DataFrame()  # Return an empty DataFrame if no piano part is found

def process_multiple_files(file_paths):
    # 데이터프레임을 저장할 리스트 생성
    dfs = []

    for file_path in file_paths:
        # 미디 파일에서 데이터프레임으로 변환
        midi_df = midi_to_dataframe(file_path)
        if not midi_df.empty:
            dfs.append(midi_df)

    # 모든 데이터프레임을 하나로 합치기
    combined_df = pd.concat(dfs, ignore_index=True)

    return combined_df

def dataframe_to_midi(dataframe, output_midi_path):
    # Create a stream to represent the MIDI file
    midi_stream = stream.Score()

    # Add a piano instrument to the stream
    piano_part = stream.Part()
    piano_part.append(instrument.Piano())  # You may need to import 'instrument' from music21

    # Add notes to the piano part from the dataframe
    for index, row in dataframe.iterrows():
        offset = row['Offset']
        pitch = row['Pitch']
        velocity = row['Velocity']

        if not pd.isnull(pitch):  # Check if it's a note (not a rest)
            n = note.Note()
            n.pitch.ps = pitch
            n.volume.velocity = velocity
            piano_part.append(n)
        else:  # It's a rest
            r = note.Rest()
            r.duration.quarterLength = row['Duration']
            piano_part.append(r)

    # Add the piano part to the MIDI stream
    midi_stream.append(piano_part)

    # Set tempo and meter (you can adjust these parameters)
    midi_stream.append(tempo.MetronomeMark(number=160))
    midi_stream.append(meter.TimeSignature('4/4'))

    # Write the stream to a MIDI file
    midi_stream.write('midi', fp=output_midi_path)

if __name__ == "__main__":
    # 여러 미디 파일 경로 지정
    midi_files = [
        '/content/drive/MyDrive/giga_bach/APTITUDE/media/getmusic_result/midi0/outputs.mid',
        '/content/drive/MyDrive/giga_bach/APTITUDE/media/getmusic_result/midi1/outputs.mid',
        '/content/drive/MyDrive/giga_bach/APTITUDE/media/getmusic_result/midi2/outputs.mid'
    ]
    
    combined_df = process_multiple_files(midi_files)

    # Output MIDI file path
    output_midi_path = '/content/drive/MyDrive/giga_bach/APTITUDE/media/getmusic_result/midi2df2midi/output_mid.mid'

    # Convert dataframe to MIDI and save
    dataframe_to_midi(combined_df, output_midi_path)
