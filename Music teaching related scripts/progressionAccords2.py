from mido import MidiFile, MidiTrack, Message, MetaMessage
import random

chord_types = {
    'maj': [0, 4, 7],
    'min': [0, 3, 7]
}

notes = {
    'Do': 60, 'Do#': 61, 'Ré': 62, 'Ré#': 63, 'Mi': 64, 'Fa': 65,
    'Fa#': 66, 'Sol': 67, 'Sol#': 68, 'La': 69, 'La#': 70, 'Si': 71
}

progressions = [
    [('Do', 'maj'), ('Sol', 'maj'), ('La', 'min'), ('Fa', 'maj')],  # Pop/Rock
    [('Do', 'maj'), ('Fa', 'maj'), ('Sol', 'maj'), ('Do', 'maj')],  # Classique
    [('La', 'min'), ('Fa', 'maj'), ('Do', 'maj'), ('Sol', 'maj')],  # Triste
    [('Ré', 'min'), ('Sol', 'maj'), ('Do', 'maj'), ('Fa', 'maj')]   # Funk/Neo-Soul
]

mid = MidiFile()
track = MidiTrack()
mid.tracks.append(track)

track.append(MetaMessage('track_name', name="Mélange progressions", time=0))
track.append(MetaMessage('set_tempo', tempo=400000, time=0))  # 150 BPM
track.append(Message('program_change', program=0, time=0))  # Piano

duration = 960 // 6  # 1/6e de noire

# Nombre de répétitions (ou accords) dans le morceau
num_chords = 32

time_acc = 0
for i in range(num_chords):
    # Choisir aléatoirement une progression
    prog = random.choice(progressions)
    # Choisir un accord dans cette progression (en boucle)
    chord = prog[i % len(prog)]
    root_name, chord_type = chord

    root = notes[root_name]
    intervals = chord_types[chord_type]
    chord_notes = [root + interval for interval in intervals]

    # Note on avec délai accumulé (0 sauf au début)
    for note in chord_notes:
        track.append(Message('note_on', note=note, velocity=80, time=0))
    # Note off après la durée (mettre time uniquement sur la première note off)
    track.append(Message('note_off', note=chord_notes[0], velocity=80, time=duration))
    for note in chord_notes[1:]:
        track.append(Message('note_off', note=note, velocity=80, time=0))

mid.save('morceau_melange.mid')
print("✅ Fichier MIDI enregistré : morceau_melange.mid")
