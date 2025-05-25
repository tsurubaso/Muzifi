from mido import Message, MidiFile, MidiTrack, MetaMessage
import os

# Accord et leurs notes (en notation européenne)
accords = [
    ("Do majeur", ["Do", "Mi", "Sol"]),
    ("Fa majeur", ["Fa", "La", "Do"]),
    ("Sol majeur", ["Sol", "Si", "Ré"]),
    
    ("Ré mineur", ["Ré", "Fa", "La"]),
    ("Mi mineur", ["Mi", "Sol", "Si"]),
    ("La mineur", ["La", "Do", "Mi"]),
    
    ("Si diminué", ["Si", "Ré", "Fa"])
]

# Correspondance notes → numéros MIDI (octave 4)
note_to_midi = {
    "Do": 60, "Do#": 61, "Réb": 61,
    "Ré": 62, "Ré#": 63, "Mib": 63,
    "Mi": 64,
    "Fa": 65, "Fa#": 66, "Solb": 66,
    "Sol": 67, "Sol#": 68, "Lab": 68,
    "La": 69, "La#": 70, "Sib": 70,
    "Si": 71
}

def notes_to_midi(notes, octave=4):
    return [note_to_midi[n] + 12 * (octave - 4) for n in notes]

def play_accord_repeated(track, notes, repeat=3, note_duration=600, velocity=90):
    midi_notes = notes_to_midi(notes)
    for _ in range(repeat):
        # all notes ON
        for n in midi_notes:
            track.append(Message('note_on', note=n, velocity=velocity, time=0))
        # all notes OFF after note_duration
        for n in midi_notes:
            track.append(Message('note_off', note=n, velocity=velocity, time=note_duration))

mid = MidiFile()
track = MidiTrack()
mid.tracks.append(track)

track.append(MetaMessage('track_name', name="Accords classiques répétés", time=0))
track.append(Message('program_change', program=0, time=0))  # Piano

# Jouer Do majeur et ses accords liés (Fa majeur, Sol majeur)
for nom, notes in [accords[0], accords[1], accords[2]]:
    print(f"Joue {nom}")
    play_accord_repeated(track, notes, repeat=3, note_duration=600)

# Pause entre groupes (environ 2 secondes, 2000 ticks)
track.append(Message('note_off', note=0, velocity=0, time=2000))

# Jouer Ré mineur et ses accords liés (Mi mineur, La mineur)
for nom, notes in [accords[3], accords[4], accords[5]]:
    print(f"Joue {nom}")
    play_accord_repeated(track, notes, repeat=3, note_duration=600)

# Pause entre groupes
track.append(Message('note_off', note=0, velocity=0, time=2000))

# Jouer Si diminué seul (dernier accord)
print(f"Joue {accords[6][0]}")
play_accord_repeated(track, accords[6][1], repeat=3, note_duration=600)

# ─────────────────────────────
# 💾 Sauvegarde sur le bureau
# ─────────────────────────────
desktop_onedrive = os.path.join(os.path.expanduser("~"), "OneDrive", "Desktop")
desktop_local = os.path.join(os.path.expanduser("~"), "Desktop")
desktop_path = desktop_onedrive if os.path.exists(desktop_onedrive) else desktop_local

file_path = os.path.join(desktop_path, "Accords_Classiques_Repetes.mid")
print(f"✅ Fichier MIDI créé : {file_path}")
mid.save(file_path)

