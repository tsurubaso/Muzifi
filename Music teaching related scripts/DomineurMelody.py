from mido import MidiFile, MidiTrack, Message, MetaMessage

# Map des noms vers valeurs MIDI
note_to_midi = {
    'Do': 60, 'Do#': 61, 'Ré': 62, 'Ré#': 63, 'Mib': 63, 'Mi': 64,
    'Fa': 65, 'Fa#': 66, 'Sol': 67, 'Sol#': 68, 'Lab': 68, 'La': 69,
    'La#': 70, 'Sib': 70, 'Si': 71
}

# Gamme de Do mineur naturelle
gamme_do_mineur = ['Do', 'Ré', 'Mib', 'Fa', 'Sol', 'Lab', 'Sib']

# Accords de la gamme (triades)
accords = [
    ('Do', 'Mib', 'Sol'),     # i
    ('Ré', 'Fa', 'Lab'),      # ii°
    ('Mib', 'Sol', 'Sib'),    # III
    ('Fa', 'Lab', 'Do'),      # iv
    ('Sol', 'Sib', 'Ré'),     # v
    ('Lab', 'Do', 'Mib'),     # VI
    ('Sib', 'Ré', 'Fa')       # VII
]

# Création MIDI
mid = MidiFile()
track_chords = MidiTrack()
track_melody = MidiTrack()
mid.tracks.append(track_chords)
mid.tracks.append(track_melody)

# Meta + tempo
tempo = 500000  # ≈120 BPM
for track in [track_chords, track_melody]:
    track.append(MetaMessage('set_tempo', tempo=tempo, time=0))

track_chords.append(MetaMessage('track_name', name="Accords", time=0))
track_melody.append(MetaMessage('track_name', name="Mélodie", time=0))

# Instruments
track_chords.append(Message('program_change', program=0, time=0))   # Piano
track_melody.append(Message('program_change', program=40, time=0))  # Violon

# Durée
chord_duration = 3 * 4 * 240  # Chaque accord dure autant que 3x4 croches
melody_duration = 240         # une croche

for i, accord in enumerate(accords):
    # ACCORDS
    notes_midi = [note_to_midi[n] for n in accord]
    for note in notes_midi:
        track_chords.append(Message('note_on', note=note, velocity=80, time=0))
    for note in notes_midi:
        track_chords.append(Message('note_off', note=note, velocity=80, time=chord_duration))

    # MÉLODIE x3 : 3 x 4 notes
    start_index = i % len(gamme_do_mineur)
    melody_pattern = [note_to_midi[gamme_do_mineur[(start_index + j) % len(gamme_do_mineur)]] for j in range(4)]

    for _ in range(3):  # répétition 3x
        for note in melody_pattern:
            track_melody.append(Message('note_on', note=note, velocity=70, time=0))
            track_melody.append(Message('note_off', note=note, velocity=70, time=melody_duration))

# Sauvegarde
output_path = "do_mineur_melodie_x3.mid"
mid.save(output_path)
print(f"✅ Fichier MIDI sauvegardé : {output_path}")
