from mido import MidiFile, MidiTrack, Message, MetaMessage

# Map des noms vers valeurs MIDI
note_to_midi = {
    'Do': 60, 'Do#': 61, 'Ré': 62, 'Ré#': 63, 'Mib': 63, 'Mi': 64,
    'Fa': 65, 'Fa#': 66, 'Sol': 67, 'Sol#': 68, 'Lab': 68, 'La': 69,
    'La#': 70, 'Sib': 70, 'Si': 71
}

# Accords de la gamme de Do mineur naturelle (Do Ré Mib Fa Sol Lab Sib)
accords = [
    ('Do', 'Mib', 'Sol'),     # i : Do mineur
    ('Ré', 'Fa', 'Lab'),      # ii° : Ré diminué
    ('Mib', 'Sol', 'Sib'),    # III : Mib majeur
    ('Fa', 'Lab', 'Do'),      # iv : Fa mineur
    ('Sol', 'Sib', 'Ré'),     # v : Sol mineur
    ('Lab', 'Do', 'Mib'),     # VI : Lab majeur
    ('Sib', 'Ré', 'Fa'),      # VII : Sib majeur
]

# Paramètres MIDI
mid = MidiFile()
track = MidiTrack()
mid.tracks.append(track)

# Infos tempo et instrument
track.append(MetaMessage('track_name', name="Accords Do mineur", time=0))
track.append(MetaMessage('set_tempo', tempo=500000, time=0))  # 120 BPM
track.append(Message('program_change', program=0, time=0))    # Piano

# Durée d'un accord (1 mesure)
accord_duration = 960

for accord in accords:
    notes_midi = [note_to_midi[n] for n in accord]
    # Note ON
    for note in notes_midi:
        track.append(Message('note_on', note=note, velocity=80, time=0))
    # Note OFF
    for note in notes_midi:
        track.append(Message('note_off', note=note, velocity=80, time=accord_duration))

# Sauvegarde
output_path = "do_mineur_naturel.mid"
mid.save(output_path)
print(f"Fichier MIDI créé : {output_path}")
