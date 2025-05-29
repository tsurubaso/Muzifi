
from mido import Message, MidiFile, MidiTrack, MetaMessage
import os

# ------------------------------
# Gamme de Do majeur : accords diatoniques I à vii°
# ------------------------------
gamme_do_majeur = [
    ("I - Do majeur", ["Do", "Mi", "Sol"]),
    ("ii - Ré mineur", ["Ré", "Fa", "La"]),
    ("iii - Mi mineur", ["Mi", "Sol", "Si"]),
    ("IV - Fa majeur", ["Fa", "La", "Do"]),
    ("V - Sol majeur", ["Sol", "Si", "Ré"]),
    ("vi - La mineur", ["La", "Do", "Mi"]),
    ("vii° - Si diminué", ["Si", "Ré", "Fa"])
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

def play_accord(track, notes, duration=600, velocity=90):
    midi_notes = notes_to_midi(notes)
    for n in midi_notes:
        track.append(Message('note_on', note=n, velocity=velocity, time=0))
    for n in midi_notes:
        track.append(Message('note_off', note=n, velocity=velocity, time=duration))

# ------------------------------
# Création du fichier MIDI
# ------------------------------
mid = MidiFile()
track = MidiTrack()
mid.tracks.append(track)

track.append(MetaMessage('track_name', name="Gamme de Do majeur (x2)", time=0))
track.append(Message('program_change', program=0, time=0))  # Piano

# ------------------------------
# Joue la gamme 2 fois avec pause de 2s entre les deux
# ------------------------------
for i in range(2):
    for nom, notes in gamme_do_majeur:
        print(f"🎵 {nom}")
        play_accord(track, notes, duration=600)
    
    if i == 0:
        # Pause de 2 secondes avant la 2e répétition
        track.append(Message('note_off', note=0, velocity=0, time=2000))

# ------------------------------
# 💾 Sauvegarde sur le bureau
# ------------------------------
desktop_onedrive = os.path.join(os.path.expanduser("~"), "OneDrive", "Desktop")
desktop_local = os.path.join(os.path.expanduser("~"), "Desktop")
desktop_path = desktop_onedrive if os.path.exists(desktop_onedrive) else desktop_local

file_path = os.path.join(desktop_path, "Gamme_Do_Majeur_x2.mid")
print(f"✅ Fichier MIDI créé : {file_path}")
mid.save(file_path)
