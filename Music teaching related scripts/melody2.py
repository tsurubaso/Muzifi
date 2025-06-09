from mido import MidiFile, MidiTrack, Message, MetaMessage

# Accords
chord_types = {
    'maj': [0, 4, 7],
    'min': [0, 3, 7]
}

notes = {
    'Do': 60, 'Do#': 61, 'Ré': 62, 'Ré#': 63, 'Mi': 64, 'Fa': 65,
    'Fa#': 66, 'Sol': 67, 'Sol#': 68, 'La': 69, 'La#': 70, 'Si': 71
}

# Progressions
progression1 = [('Do', 'maj'), ('Sol', 'maj'), ('La', 'min'), ('Fa', 'maj')]
progression2 = [('Do', 'maj'), ('Fa', 'maj'), ('Sol', 'maj'), ('Do', 'maj')]

# Forme : A → B → A
structure = progression1 + progression2 + progression1

# Mélodie simple
melody = [64, 65, 67, 69, 67, 65, 64, 62]  # Mi Fa Sol La Sol Fa Mi Ré

# MIDI setup
mid = MidiFile()
chords_track = MidiTrack()
melody_track = MidiTrack()
mid.tracks.append(chords_track)
mid.tracks.append(melody_track)

# Tempo et instruments
chords_track.append(MetaMessage('track_name', name="Accords", time=0))
chords_track.append(MetaMessage('set_tempo', tempo=400000, time=0))
chords_track.append(Message('program_change', program=0, time=0))  # Piano

melody_track.append(MetaMessage('track_name', name="Mélodie", time=0))
melody_track.append(Message('program_change', program=40, time=0))  # Violin

# Durées
chord_duration = 960 // 3  # 1/3 de noire
melody_duration = 160      # 1/6 de noire

# Accords (structure complète)
for root_name, chord_type in structure:
    root = notes[root_name]
    intervals = chord_types[chord_type]
    chord_notes = [root + interval for interval in intervals]
    for note in chord_notes:
        chords_track.append(Message('note_on', note=note, velocity=80, time=0))
    for note in chord_notes:
        chords_track.append(Message('note_off', note=note, velocity=80, time=chord_duration))

# Mélodie répétée 9 fois
for _ in range(9):
    for note in melody:
        melody_track.append(Message('note_on', note=note, velocity=100, time=0))
        melody_track.append(Message('note_off', note=note, velocity=100, time=melody_duration))

# Save
mid.save('composition_ABA_melody_loop.mid')
print("✅ Fichier MIDI enregistré : composition_ABA_melody_loop.mid")
