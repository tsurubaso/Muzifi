from mido import MidiFile, MidiTrack, Message

# Création du fichier MIDI
mid = MidiFile()
track = MidiTrack()
mid.tracks.append(track)

# Ajout du tempo et instrument (piano par défaut)
track.append(Message('program_change', program=1, time=0))  

# Notes MIDI de la gamme pentatonique majeure de Do (Do-Ré-Mi-Sol-La)
notes = [60, 62, 64, 67, 69]  # Correspondances MIDI pour Do, Ré, Mi, Sol, La

# Ajout des notes MIDI
for note in notes:
    track.append(Message('note_on', note=note, velocity=64, time=0))
    track.append(Message('note_off', note=note, velocity=64, time=480))  # Durée d'une noire

# Sauvegarde du fichier MIDI
midi_path = "gamme_pentatonique_do_majeur.mid"
mid.save(midi_path)
print(f"✅ Fichier MIDI enregistré : {midi_path}")
