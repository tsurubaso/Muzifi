from mido import Message, MidiFile, MidiTrack

# Création du fichier MIDI
mid = MidiFile()

# Instruments MIDI (General MIDI program numbers)
instruments = {
    'piano': 0,    # Acoustic Grand Piano
    'guitar': 24,  # Nylon Guitar
    'bass': 32,    # Acoustic Bass
    'strings': 48  # String Ensemble 1
}

# Canaux MIDI (0-15)
channels = {
    'piano': 0,
    'guitar': 1,
    'bass': 2,
    'strings': 3
}

# Création de 4 pistes, une par instrument
tracks = {}
for name in instruments:
    track = MidiTrack()
    track.append(Message('program_change', program=instruments[name], channel=channels[name], time=0))
    tracks[name] = track
    mid.tracks.append(track)

# Motif simple : Do-Mi-Sol / Fa-La-Do / Sol-Si-Ré / Do
# Do majeur (C major): C = 60
pattern_major = [
    [60, 64, 67],  # C major chord
    [65, 69, 72],  # F major chord
    [67, 71, 74],  # G major chord
    [60]           # C
]

# La mineur (A minor): A = 57 (relative minor of C)
pattern_minor = [
    [57, 60, 64],  # A minor chord
    [62, 65, 69],  # D minor chord
    [64, 67, 71],  # E minor chord
    [57]           # A
]

# Durée d'une noire (480 ticks)
note_duration = 480
rest_duration = 60

def add_chords_to_track(track, chords, channel, start_offset=0):
    time = start_offset
    for chord in chords:
        for note in chord:
            track.append(Message('note_on', note=note, velocity=64, time=time, channel=channel))
            time = 0
        for note in chord:
            track.append(Message('note_off', note=note, velocity=64, time=note_duration, channel=channel))

# Partie majeure
for name in tracks:
    add_chords_to_track(tracks[name], pattern_major, channels[name])

# Pause
pause_ticks = 480 * 2
for name in tracks:
    tracks[name].append(Message('note_off', note=0, velocity=0, time=pause_ticks, channel=channels[name]))

# Partie mineure
for name in tracks:
    add_chords_to_track(tracks[name], pattern_minor, channels[name])

# Sauvegarde
mid.save("majeur_vs_mineur_multiinstrument.mid")
print("✅ Fichier MIDI enregistré sous 'majeur_vs_mineur_multiinstrument.mid'")
