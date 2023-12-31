pos_resolution = 4 # 16  # per beat (quarter note)
bar_max = 32
velocity_quant = 4
tempo_quant = 12  # 2 ** (1 / 12)
min_tempo = 16
max_tempo = 256
duration_max = 4  # 2 ** 8 * beat
max_ts_denominator = 6  # x/1 x/2 x/4 ... x/64
max_notes_per_bar = 1  # 1/64 ... 128/64 # 
beat_note_factor = 4  # In MIDI format a note is always 4 beats
deduplicate = True
filter_symbolic = False
filter_symbolic_ppl = 16
trunc_pos = 2 ** 16  # approx 30 minutes (1024 measures)
sample_len_max = 1024  # window length max
sample_overlap_rate = 1.5
ts_filter = True
pool_num = 200
max_inst = 127
max_pitch = 127
max_velocity = 127
tracks_start = [16, 144, 997, 5366, 6921, 10489]
tracks_end = [143, 996, 5365, 6920, 10488, 11858]
