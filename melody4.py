from mido import MidiFile, MidiTrack, Message, MetaMessage

note_to_midi = {
    'Do': 60, 'Ré': 62, 'Mi': 64, 'Fa': 65, 'Sol': 67, 'La': 69, 'Si': 71
}

# Gamme de Do majeur
scale = ['Do', 'Ré', 'Mi', 'Fa', 'Sol', 'La', 'Si']

# Progression d'accords
chords = [
    ('Do', ['Do', 'Mi', 'Sol']),
    ('Fa', ['Fa', 'La', 'Do']),
    ('Sol', ['Sol', 'Si', 'Ré']),
    ('Do', ['Do', 'Mi', 'Sol'])
]

# Mélodie : Motif de 4 notes basé sur la gamme (Do → Ré → Mi → Sol)
melody_motif = ['Do', 'Ré', 'Mi', 'Sol']

# Répéter ce motif avec quelques variations et résolutions
melody_phrases = [
    melody_motif,
    ['Mi', 'Ré', 'Fa', 'Sol'],     # Variation 1
    ['Mi', 'Sol', 'Fa', 'Mi'],     # Variation 2
    ['Do', 'Ré', 'Mi', 'Do']       # Résolution
]

# Création fichier MIDI
mid = MidiFile()
chord_track = MidiTrack()
melody_track = MidiTrack()
mid.tracks.append(chord_track)
mid.tracks.append(melody_track)

# Meta infos
tempo = 500000  # ~120 BPM
chord_track.append(MetaMessage('track_name', name="Accords", time=0))
melody_track.append(MetaMessage('track_name', name="Mélodie", time=0))
chord_track.append(MetaMessage('set_tempo', tempo=tempo, time=0))
melody_track.append(MetaMessage('set_tempo', tempo=tempo, time=0))

# Instruments
chord_track.append(Message('program_change', program=0, time=0))  # Piano
melody_track.append(Message('program_change', program=40, time=0))  # Violin

# Durées
chord_duration = 480  # noire
note_duration = 480  # croche

# Construction des pistes
for i, (chord_name, chord_notes) in enumerate(chords):
    # ACCORD
    midi_notes = [note_to_midi[n] for n in chord_notes]
    for note in midi_notes:
        chord_track.append(Message('note_on', note=note, velocity=80, time=0))
    for note in midi_notes:
        chord_track.append(Message('note_off', note=note, velocity=80, time=chord_duration))

    # MÉLODIE : motif correspondant à la mesure
    phrase = melody_phrases[i % len(melody_phrases)]
    for note_name in phrase:
        note = note_to_midi[note_name]
        melody_track.append(Message('note_on', note=note, velocity=70, time=0))
        melody_track.append(Message('note_off', note=note, velocity=70, time=note_duration))

# Sauvegarde
output_path = "melodie_structurée_do_majeur.mid"
mid.save(output_path)
