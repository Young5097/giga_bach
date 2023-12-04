import mido
import pretty_midi

def identify_instruments(midi_file_path):
    midi_data = mido.MidiFile(midi_file_path)
    midi_pretty_format = pretty_midi.PrettyMIDI(midi_file_path)

    instruments_used = set()

    for i, track in enumerate(midi_data.tracks):
        for msg in track:
            if msg.type == 'program_change':
                program = msg.program
                instruments_used.add(program)

    instrument_mapping = {
        32: 'b',  # Bass
        128: 'd',  # Drums
        25: 'g',  # Guitar
        80: 'l',  # Lead
        0: 'p',   # Piano
        48: 's',  # Strings
        29: 'c'   # Chords
    }

    instrument_symbols = [instrument_mapping.get(program, 'unknown') for program in instruments_used]

    return instrument_symbols


if __name__ == "__main__":
    midi_file_path = "/content/drive/MyDrive/AI_composer/p2bdg-Super_Mario_Bros.__Main_Theme.mid"  # 미디 파일 경로를 지정하세요
    instruments = identify_instruments(midi_file_path)

    print("Instruments used in the MIDI file:")
    for instrument in instruments:
        print(instrument)







