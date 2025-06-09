from mido import MidiFile, MidiTrack, Message, MetaMessage

# Accord vers gamme et suggestions de mélodies (notes par nom)
chord_types = {
    'maj': [0, 4, 7],   # Majeur
    'min': [0, 3, 7]    # Mineur
}

# Gammes majeures associées à chaque note
major_scales = {
    'Do':     ['Do', 'Ré', 'Mi', 'Fa', 'Sol', 'La', 'Si'],
    'Do#':    ['Do#', 'Ré#', 'Fa', 'Fa#', 'Sol#', 'La#', 'Do'],
    'Ré':     ['Ré', 'Mi', 'Fa#', 'Sol', 'La', 'Si', 'Do#'],
    'Ré#':    ['Ré#', 'Fa', 'Sol', 'Sol#', 'La#', 'Do', 'Ré'],
    'Mi':     ['Mi', 'Fa#', 'Sol#', 'La', 'Si', 'Do#', 'Ré#'],
    'Fa':     ['Fa', 'Sol', 'La', 'La#', 'Do', 'Ré', 'Mi'],
    'Fa#':    ['Fa#', 'Sol#', 'La#', 'Si', 'Do#', 'Ré#', 'Fa'],
    'Sol':    ['Sol', 'La', 'Si', 'Do', 'Ré', 'Mi', 'Fa#'],
    'Sol#':   ['Sol#', 'La#', 'Do', 'Do#', 'Ré#', 'Fa', 'Sol'],
    'La':     ['La', 'Si', 'Do#', 'Ré', 'Mi', 'Fa#', 'Sol#'],
    'La#':    ['La#', 'Do', 'Ré', 'Ré#', 'Fa', 'Sol', 'La'],
    'Si':     ['Si', 'Do#', 'Ré#', 'Mi', 'Fa#', 'Sol#', 'La#']
}

# Conversion note -> valeur MIDI
note_to_midi = {
    'Do': 60, 'Do#': 61, 'Ré': 62, 'Ré#': 63, 'Mi': 64, 'Fa': 65,
    'Fa#': 66, 'Sol': 67, 'Sol#': 68, 'La': 69, 'La#': 70, 'Si': 71
}

# Exemple de progression
progression = [
    ('Do', 'maj'),
    ('Sol', 'maj'),
    ('La', 'min'),
    ('Fa', 'maj')
]

# Création fichier MIDI
mid = MidiFile()
chord_track = MidiTrack()
melody_track = MidiTrack()
mid.tracks.append(chord_track)
mid.tracks.append(melody_track)

# Meta
chord_track.append(MetaMessage('track_name', name="Accords", time=0))
melody_track.append(MetaMessage('track_name', name="Mélodie", time=0))
tempo = 400000  # 150 BPM
chord_track.append(MetaMessage('set_tempo', tempo=tempo, time=0))
melody_track.append(MetaMessage('set_tempo', tempo=tempo, time=0))

# Instrument
chord_track.append(Message('program_change', program=0, time=0))  # Piano
melody_track.append(Message('program_change', program=1, time=0))  # Autre instrument pour la mélodie

# Durées
chord_duration = 960  # une noire
melody_duration = 240  # une croche
melody_repeats = 3     # <- Nombre de répétitions de la mélodie

for root_name, chord_type in progression:
    # ACCORD
    root_midi = note_to_midi[root_name]
    intervals = chord_types[chord_type]
    chord_notes = [root_midi + i for i in intervals]

    for note in chord_notes:
        chord_track.append(Message('note_on', note=note, velocity=80, time=0))
    for note in chord_notes:
        chord_track.append(Message('note_off', note=note, velocity=80, time=chord_duration))

    # MÉLODIE répétée
    scale = major_scales[root_name]
    melody_notes = [note_to_midi[n] for n in scale[:4]]  # 4 premières notes de la gamme

    for _ in range(melody_repeats):
        for note in melody_notes:
            melody_track.append(Message('note_on', note=note, velocity=70, time=0))
            melody_track.append(Message('note_off', note=note, velocity=70, time=melody_duration))

# Sauvegarde
output_path = "melodie_accords_repeats.mid"
mid.save(output_path)
