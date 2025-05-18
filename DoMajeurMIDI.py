from mido import MidiFile, MidiTrack, Message

# Création du fichier MIDI
mid = MidiFile()
track = MidiTrack()
mid.tracks.append(track)

# Ajout du tempo (120 BPM)
track.append(Message('program_change', program=1, time=0))  # Instrument: Piano

# Fréquences MIDI de la gamme Do majeur (C4 → C5)
#notes = [60, 62, 64, 65, 67, 69, 71, 72]  # Do, Ré, Mi, Fa, Sol, La, Si, Do

#notes = [69, 71, 72, 74, 76, 77, 79, 81]  # La Si Do Ré Mi Fa Sol La 

#notes = [67, 69, 71, 72, 74, 76, 78, 79]  # Sol La Si Do Ré Mi Fa# Sol

notes = [64, 66, 67, 69, 71, 72, 74, 76]  # Mi Fa# Sol La Si Do Ré Mi

# Ajout des notes MIDI
for note in notes:
    track.append(Message('note_on', note=note, velocity=64, time=0))
    track.append(Message('note_off', note=note, velocity=64, time=480))  # Durée d'une noire

# Sauvegarde du fichier MIDI
midi_path = "gamme_do_majeur.mid"
#mid.save(midi_path)
#print(f"✅ Fichier MIDI enregistré : {midi_path}")

#mid.save("gamme_la_mineur.mid")
#print("✅ Fichier : gamme_la_mineur.mid")


#mid.save("gamme_sol_majeur.mid")
#print("✅ Fichier : gamme_sol_majeur.mid")

mid.save("gamme_mi_mineur.mid")
print("✅ Fichier : gamme_mi_mineur.mid")
