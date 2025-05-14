import os
from mido import MidiFile, MidiTrack, Message, MetaMessage

# === 1. Demande le dossier à l'utilisateur ===
folder = input("📁 Entrez le chemin du dossier contenant les fichiers MIDI : ").strip()

if not os.path.isdir(folder):
    print("❌ Dossier invalide.")
    exit()

# === 2. Liste les fichiers MIDI ===
midi_files = [f for f in os.listdir(folder) if f.endswith(".mid")]
if not midi_files:
    print("❌ Aucun fichier MIDI trouvé dans ce dossier.")
    exit()

# === 3. Instruments arbitraires (General MIDI) ===
instrument_list = [0, 24, 32, 40, 48, 56, 64, 73, 80, 88]  # piano, guitar, bass, strings, etc.

# === 4. Crée le fichier MIDI combiné ===
combined = MidiFile()
combined.ticks_per_beat = 480  # Valeur standard


for i, filename in enumerate(midi_files):
    path = os.path.join(folder, filename)
    midi = MidiFile(path)

    track = MidiTrack()
    combined.tracks.append(track)

    # Nom de piste
    track_name = os.path.splitext(filename)[0]
    track.append(MetaMessage('track_name', name=track_name, time=0))

    # Instrument (program_change)
    instrument = instrument_list[i % len(instrument_list)]
    track.append(Message('program_change', program=instrument, time=0))

    # Copie les messages depuis le premier track du fichier
    for msg in midi.tracks[0]:
        if not msg.is_meta:
            track.append(msg.copy(time=msg.time))

# === 5. Sauvegarde du fichier fusionné ===
output_path = os.path.join(folder, "fusion_midis_output.mid")
combined.save(output_path)
print(f"\n✅ Fichier combiné enregistré : {output_path}")
