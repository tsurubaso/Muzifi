from mido import MidiFile, MidiTrack, Message, MetaMessage

# Map noms → MIDI
note_to_midi = {
    'Do': 60, 'Do#': 61, 'Ré': 62, 'Ré#': 63, 'Mi': 64,
    'Fa': 65, 'Fa#': 66, 'Sol': 67, 'Sol#': 68, 'La': 69,
    'La#': 70, 'Si': 71
}

# Gamme de Do majeur
gamme_do_majeur = ['Do', 'Ré', 'Mi', 'Fa', 'Sol', 'La', 'Si']

# Accords triadiques de la gamme de Do majeur
accords = [
    ('Do', 'Mi', 'Sol'),     # I
    ('Ré', 'Fa', 'La'),      # ii
    ('Mi', 'Sol', 'Si'),     # iii
    ('Fa', 'La', 'Do'),      # IV
    ('Sol', 'Si', 'Ré'),     # V
    ('La', 'Do', 'Mi'),      # vi
    ('Si', 'Ré', 'Fa')       # vii°
]

# Durées
melody_duration = 240
notes_melody_total = len(accords) * 12  # 12 croches par accord (3 motifs x 4 notes)

# Création fichier MIDI
mid = MidiFile()
track_chords = MidiTrack()
track_melody = MidiTrack()
mid.tracks.append(track_chords)
mid.tracks.append(track_melody)

# Meta et tempo
tempo = 500000
for track in [track_chords, track_melody]:
    track.append(MetaMessage('set_tempo', tempo=tempo, time=0))

track_chords.append(MetaMessage('track_name', name="Accords", time=0))
track_melody.append(MetaMessage('track_name', name="Mélodie", time=0))

# Instruments
track_chords.append(Message('program_change', program=0, time=0))   # Piano
track_melody.append(Message('program_change', program=40, time=0))  # Violon

# ACCORDS
chord_duration = 12 * melody_duration  # correspond à 12 croches (3 motifs)

for accord in accords:
    notes = [note_to_midi[n] for n in accord]
    for note in notes:
        track_chords.append(Message('note_on', note=note, velocity=80, time=0))
    for note in notes:
        track_chords.append(Message('note_off', note=note, velocity=80, time=chord_duration))

# MÉLODIE continue
melody_pattern = [note_to_midi[n] for n in gamme_do_majeur]
melody_len = len(melody_pattern)

for i in range(notes_melody_total):
    note = melody_pattern[i % melody_len]
    track_melody.append(Message('note_on', note=note, velocity=70, time=0))
    track_melody.append(Message('note_off', note=note, velocity=70, time=melody_duration))

# Sauvegarde
output_path = "do_majeur_melodie_continue.mid"
mid.save(output_path)
print(f"✅ Fichier MIDI sauvegardé : {output_path}")
