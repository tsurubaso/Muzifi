from mido import MidiFile, MidiTrack, Message, MetaMessage

note_to_midi = {
    'Do': 60, 'Ré': 62, 'Mi': 64, 'Fa': 65, 'Sol': 67, 'La': 69, 'Si': 71
}

# Phrase principale
motif = ['Do', 'Ré', 'Mi', 'Sol']

# Mélodie complète avec variations
melody_phrases = [
    motif,                             # Motif de base
    ['Mi', 'Ré', 'Fa', 'Sol'],         # Variation 1
    ['Mi', 'Sol', 'Fa', 'Mi'],         # Variation 2
    ['Do', 'Ré', 'Mi', 'Do'],           # Résolution
    ['Mi', 'Ré', 'Fa', 'Sol'],         # Variation 1
    ['Mi', 'Sol', 'Fa', 'Mi'],         # Variation 2
    ['Do', 'Ré', 'Mi', 'Do'],           # Résolution
    ['Mi', 'Ré', 'Fa', 'Sol'],         # Variation 1
    ['Mi', 'Sol', 'Fa', 'Mi'],         # Variation 2
    ['Do', 'Ré', 'Mi', 'Do'] ,
             motif         # Résolution
]

# Création fichier MIDI
mid = MidiFile()
melody_track = MidiTrack()
mid.tracks.append(melody_track)

# Métadonnées
tempo = 500000  # ~120 BPM
melody_track.append(MetaMessage('track_name', name="Mélodie seule", time=0))
melody_track.append(MetaMessage('set_tempo', tempo=tempo, time=0))
melody_track.append(Message('program_change', program=41, time=0))  # Piano ou violon

# Durée des notes
note_duration = 240  # croche

# Écriture de la mélodie
for phrase in melody_phrases:
    for note_name in phrase:
        midi_note = note_to_midi[note_name]
        melody_track.append(Message('note_on', note=midi_note, velocity=70, time=0))
        melody_track.append(Message('note_off', note=midi_note, velocity=70, time=note_duration))

# Sauvegarde
output_path = "melodie_simple_do_majeur.mid"
mid.save(output_path)



