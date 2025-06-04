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

# Choisis ta progression ici :

#Pop/Rock (très courant)	Do – Sol – La mineur – Fa	I – V – vi – IV
progression1 = [
    ('Do', 'maj'),
    ('Sol', 'maj'),
    ('La', 'min'),
    ('Fa', 'maj')
]

#Classique / romantique	Do – Fa – Sol – Do	I – IV – V – I
progression2 = [
    ('Do', 'maj'),
    ('Fa', 'maj'),
    ('Sol', 'maj'),
    ('Do', 'maj')
]

#Triste/mélancolique	La mineur – Fa – Do – Sol	vi – IV – I – V
progression3 = [
    ('La', 'min'),
    ('Fa', 'maj'),
    ('Do', 'maj'),
    ('Sol', 'maj')
]

#Funk/Neo-Soul	Ré mineur – Sol – Do – Fa	ii – V – I – IV
progression = [
    ('Ré', 'min'),
    ('Sol', 'maj'),
    ('Do', 'maj'),
    ('Fa', 'maj')
]


# Création du fichier MIDI
mid = MidiFile()
track = MidiTrack()
mid.tracks.append(track)

# Configuration
track.append(MetaMessage('track_name', name="Progression rapide", time=0))
track.append(MetaMessage('set_tempo', tempo=400000, time=0))  # 150 BPM
track.append(Message('program_change', program=0, time=0))  # Piano

# Durée réduite (1/6e de noire)
duration = 960 // 6  # = 160 ticks

# Ajouter les accords
for root_name, chord_type in progression:
    root = notes[root_name]
    intervals = chord_types[chord_type]
    chord_notes = [root + interval for interval in intervals]

    for note in chord_notes:
        track.append(Message('note_on', note=note, velocity=80, time=0))
    for note in chord_notes:
        track.append(Message('note_off', note=note, velocity=80, time=duration))

# Sauvegarde
mid.save('progression_rapide.mid')
print("✅ Fichier MIDI enregistré : progression_rapide.mid")


