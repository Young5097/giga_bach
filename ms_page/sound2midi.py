# 사용자에게 사운드(휘파람 or 흥얼거림)를 입력 받아 midi 파일로 처리할 부분
# 사운드를 미디로 처리한 다음 임시폴더에 저장 -> getmusic
# 미디 파일 자체를 올리면 그대로 임시폴더에 저장 -> getmusic
# getmusic으로 음원을 생성하고 -> museformer 음원을 길게 늘릴늘림 -> 늘린 노래가 나오면 얘를 홈페이지에서 재생


import librosa
import librosa.display
import numpy as np
import pandas as pd
from music21 import converter, note, stream, environment, instrument
from midi2audio import FluidSynth
from midiutil import MIDIFile


def sound2midi(audio_path):  # 오디오 파일 경로 -> input_sound에서 휘파람이나 흥얼거림 노래 파일을 받아옴
    # hertz2keys 데이터프레임 정의
    hertz2keys = pd.DataFrame(
        {
            "A": [
                27.50,
                55.00,
                110.00,
                220.00,
                440.00,
                880.00,
                1760.00,
                3520.00,
                7040.00,
            ],
            "B": [
                30.87,
                61.74,
                123.47,
                246.94,
                493.88,
                987.77,
                1975.53,
                3951.07,
                7902.13,
            ],
            "Bb": [
                29.14,
                58.27,
                116.54,
                233.08,
                466.16,
                932.33,
                1864.66,
                3729.31,
                7458.62,
            ],
            "C": [
                16.35,
                32.70,
                65.41,
                130.81,
                261.63,
                523.25,
                1046.50,
                2093.00,
                4186.01,
            ],
            "C#": [
                17.32,
                34.65,
                69.30,
                138.59,
                277.18,
                554.37,
                1108.73,
                2217.46,
                4434.92,
            ],
            "D": [
                18.35,
                36.71,
                73.42,
                146.83,
                293.66,
                587.33,
                1174.66,
                2349.32,
                4698.64,
            ],
            "D#": [
                19.45,
                38.89,
                77.78,
                155.56,
                311.13,
                622.25,
                1244.51,
                2489.02,
                4978.03,
            ],
            "E": [
                20.60,
                41.20,
                82.41,
                164.81,
                329.63,
                659.26,
                1318.51,
                2637.02,
                5274.04,
            ],
            "F": [
                21.83,
                43.65,
                87.31,
                174.61,
                349.23,
                698.46,
                1396.91,
                2793.83,
                5587.65,
            ],
            "F#": [
                23.12,
                46.25,
                92.50,
                185.00,
                369.99,
                739.99,
                1479.98,
                2959.96,
                5919.91,
            ],
            "G": [
                24.50,
                49.00,
                98.00,
                196.00,
                392.00,
                783.99,
                1567.98,
                3135.96,
                6271.93,
            ],
            "G#": [
                25.96,
                51.91,
                103.83,
                207.65,
                415.30,
                830.61,
                1661.22,
                3322.44,
                6644.88,
            ],
        },
        index=["0", "1", "2", "3", "4", "5", "6", "7", "8"],
    )

    # 오디오 불러오기
    y, sr = librosa.load(audio_path, sr=None)

    # 슬라이싱 간격 설정 (0.01초)
    slice_duration = 0.05
    slice_samples = int(slice_duration * sr)

    # FFT를 위한 윈도우 크기 설정
    n_fft = 2048

    # 결과를 저장할 데이터프레임 생성
    result_df = pd.DataFrame(columns=["start_time", "end_time", "key"])

    for i in range(0, len(y), slice_samples):
        # 슬라이싱된 오디오 데이터
        audio_slice = y[i : i + slice_samples]

        # FFT 적용
        spectrum = np.abs(librosa.stft(audio_slice, n_fft=n_fft))

        # 슬라이싱된 부분에서 주파수가 가장 큰 부분 추출
        max_freq_index = np.argmax(np.sum(spectrum, axis=1))

        # 주파수가 0이 아니라면 처리
        if max_freq_index > 0:
            # 해당 주파수에 대응되는 계이름 찾기
            hz = max_freq_index * sr / n_fft

            # 주파수에 대응되는 키 찾기
            key = None
            min_diff = float("inf")
            for column in hertz2keys.columns:
                diff = np.abs(hz - hertz2keys[column].values)
                min_index = np.argmin(diff)

                if diff[min_index] < min_diff:
                    min_diff = diff[min_index]
                    key = f"{column}{hertz2keys.index[min_index]}"

            # 결과 데이터프레임에 추가
            result_df = pd.concat(
                [
                    result_df,
                    pd.DataFrame(
                        {
                            "start_time": [i / sr],
                            "end_time": [(i + slice_samples) / sr],
                            "key": [key] if key else ["Unknown"],
                        }
                    ),
                ],
                ignore_index=True,
            )
        else:
            # 주파수가 0인 경우 'Unknown'으로 처리
            result_df = pd.concat(
                [
                    result_df,
                    pd.DataFrame(
                        {
                            "start_time": [i / sr],
                            "end_time": [(i + slice_samples) / sr],
                            "key": ["Unknown"],
                        }
                    ),
                ],
                ignore_index=True,
            )

    # 연속으로 나오는 같은 음표를 합치기 위한 임계값 설정 (예: 0.1초)
    threshold = 0.25

    # 새로운 데이터프레임 생성
    combined_df = pd.DataFrame(columns=["start_time", "end_time", "key"])

    # 초기 값 설정
    current_start_time = result_df.loc[0, "start_time"]
    current_end_time = result_df.loc[0, "end_time"]
    current_key = result_df.loc[0, "key"]

    # 결과 데이터프레임을 순회하면서 연속 음표 합치기
    for index, row in result_df.iloc[1:].iterrows():
        if (
            row["start_time"] - current_end_time <= threshold
            and row["key"] == current_key
        ):
            # 현재 음표를 연장
            current_end_time = row["end_time"]
        else:
            # 새로운 음표 시작
            combined_df = pd.concat(
                [
                    combined_df,
                    pd.DataFrame(
                        {
                            "start_time": [current_start_time],
                            "end_time": [current_end_time],
                            "key": [current_key],
                        }
                    ),
                ],
                ignore_index=True,
            )

            # 초기 값 갱신
            current_start_time = row["start_time"]
            current_end_time = row["end_time"]
            current_key = row["key"]

    # 마지막 음표 추가
    combined_df = pd.concat(
        [
            combined_df,
            pd.DataFrame(
                {
                    "start_time": [current_start_time],
                    "end_time": [current_end_time],
                    "key": [current_key],
                }
            ),
        ],
        ignore_index=True,
    )
    
    # MIDI 파일 생성을 위한 설정
    midi_stream = stream.Stream()
    midi_stream.append(note.Rest())  # 아무 소리도 나지 않는 레스트 추가

    # 키에 따라 MIDI 이벤트 추가
    for index, row in combined_df.iterrows():
        key = row['key']

        # 'Unknown' 값이 아닌 경우에만 MIDI 노트 이벤트 추가
        if key != 'Unknown':
            start_time = row['start_time']
            end_time = row['end_time']

            # MIDI 노트 이벤트 추가
            midi_stream.append(note.Note(key, quarterLength=end_time - start_time))

    ################################################################################
    # MIDI 파일 저장 # got_temp_midi로 저장하게 만들기
    midi_stream.write("midi", fp="APTITUDE/media/got_temp_midi/outputs.mid")
    ################################################################################
