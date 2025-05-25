from mido import Message, MidiFile, MidiTrack, MetaMessage
import os

# ─────────────────────────────
# 🎹 Configuration des gammes majeures (notation européenne)
# ─────────────────────────────
gammes_majeures = [
    ("Do majeur", ["Do", "Ré", "Mi", "Fa", "Sol", "La", "Si"]),
    ("Ré majeur", ["Ré", "Mi", "Fa#", "Sol", "La", "Si", "Do#"]),
    ("Mi majeur", ["Mi", "Fa#", "Sol#", "La", "Si", "Do#", "Ré#"]),
    ("Fa majeur", ["Fa", "Sol", "La", "Sib", "Do", "Ré", "Mi"]),
    ("Sol majeur", ["Sol", "La", "Si", "Do", "Ré", "Mi", "Fa#"]),
    ("La majeur", ["La", "Si", "Do#", "Ré", "Mi", "Fa#", "Sol#"]),
    ("Si majeur", ["Si", "Do#", "Ré#", "Mi", "Fa#", "Sol#", "La#"]),
]

# ─────────────────────────────
# 🎼 Dictionnaire des noms de notes → numéros MIDI
# ─────────────────────────────
note_to_midi = {
    "Do": 60,  "Do#": 61, "Réb": 61,
    "Ré": 62,  "Ré#": 63, "Mib": 63,
    "Mi": 64,
    "Fa": 65,  "Fa#": 66, "Solb": 66,
    "Sol": 67, "Sol#": 68, "Lab": 68,
    "La": 69,  "La#": 70, "Sib": 70,
    "Si": 71
}

# ─────────────────────────────
# 🛠️ Fonctions utilitaires
# ─────────────────────────────
def notes_to_midi(notes, octave=4):
    return [note_to_midi[n] + 12 * (octave - 4) for n in notes]

def add_notes(track, notes, duration, velocity=80):
    for note in notes:
        track.append(Message('note_on', note=note, velocity=velocity, time=0))
        track.append(Message('note_off', note=note, velocity=velocity, time=duration))

def add_pause(track, duration):
    track.append(Message('note_off', note=0, velocity=0, time=duration))

# ─────────────────────────────
# 🎼 Création du fichier MIDI
# ─────────────────────────────
mid = MidiFile()
track = MidiTrack()
mid.tracks.append(track)

track.append(MetaMessage('track_name', name="Gammes & Accords Majeurs", time=0))
track.append(Message('program_change', program=0, time=0))  # Piano

for gamme_name, notes in gammes_majeures:
    gamme_midi = notes_to_midi(notes)

    # Gamme normale (0.5s/note)
    add_notes(track, gamme_midi, duration=240)
    add_pause(track, duration=240)  # 0.5s de pause

    # Gamme lente (1s/note)
    add_notes(track, gamme_midi, duration=480)
    add_pause(track, duration=240)  # 0.5s de pause

    # Gamme normale à nouveau
    add_notes(track, gamme_midi, duration=240)

    # Pause plus longue entre gamme et accords
    add_pause(track, duration=480)  # 1 seconde

    # Accord (1s), répété 2 fois
    accord_midi = notes_to_midi([notes[0], notes[2], notes[4]])
    for _ in range(2):
        for note in accord_midi:
            track.append(Message('note_on', note=note, velocity=100, time=0))
        for note in accord_midi:
            track.append(Message('note_off', note=note, velocity=100, time=480))

    # Pause de 5 secondes avant la prochaine gamme
    add_pause(track, duration=2400)

# ─────────────────────────────
# 💾 Sauvegarde sur le bureau
# ─────────────────────────────
desktop_onedrive = os.path.join(os.path.expanduser("~"), "OneDrive", "Desktop")
desktop_local = os.path.join(os.path.expanduser("~"), "Desktop")
desktop_path = desktop_onedrive if os.path.exists(desktop_onedrive) else desktop_local

file_path = os.path.join(desktop_path, "Gammes_Accords_Majeurs.mid")
mid.save(file_path)

print(f"\n✅ Fichier MIDI sauvegardé : {file_path}")
