from mido import MidiFile, MidiTrack, Message, MetaMessage

# Majeur = [0, 4, 7], mineur = [0, 3, 7]
chord_types = {
    'maj': [0, 4, 7],
    'min': [0, 3, 7]
}

# Dictionnaire des notes en notation européenne
notes = {
    'Do': 60, 'Do#': 61, 'Ré': 62, 'Ré#': 63, 'Mi': 64, 'Fa': 65,
    'Fa#': 66, 'Sol': 67, 'Sol#': 68, 'La': 69, 'La#': 70, 'Si': 71
}

# Progression choisie
progression = [
    ('Ré', 'min'),
    ('Sol', 'maj'),
    ('Do', 'maj'),
    ('Fa', 'maj')
]

# Mélodie simple basée sur la gamme de Do majeur
melody = [64, 65, 67, 69, 67, 65, 64, 62]  # Mi Fa Sol La Sol Fa Mi Ré

# Création du fichier MIDI
mid = MidiFile()
chords_track = MidiTrack()
melody_track = MidiTrack()
mid.tracks.append(chords_track)
mid.tracks.append(melody_track)

# Configuration générale
chords_track.append(MetaMessage('track_name', name="Accords", time=0))
chords_track.append(MetaMessage('set_tempo', tempo=400000, time=0))
chords_track.append(Message('program_change', program=0, time=0))  # Piano

melody_track.append(MetaMessage('track_name', name="Mélodie", time=0))
melody_track.append(Message('program_change', program=40, time=0))  # Violin or another lead instrument

# Durées
chord_duration = 960 // 3  # 1/3 de noire
melody_duration = 160      # 1/6 de noire

# Ajout des accords
for root_name, chord_type in progression:
    root = notes[root_name]
    intervals = chord_types[chord_type]
    chord_notes = [root + interval for interval in intervals]

    for note in chord_notes:
        chords_track.append(Message('note_on', note=note, velocity=80, time=0))
    for note in chord_notes:
        chords_track.append(Message('note_off', note=note, velocity=80, time=chord_duration))

# Ajout de la mélodie deux fois
for _ in range(3):
    for note in melody:
        melody_track.append(Message('note_on', note=note, velocity=100, time=0))
        melody_track.append(Message('note_off', note=note, velocity=100, time=melody_duration))

# Sauvegarde
mid.save('progression_avec_melodie_loop.mid')
print("✅ Fichier MIDI enregistré : progression_avec_melodie_loop.mid")
