from mido import MidiFile, MidiTrack, Message, MetaMessage, bpm2tempo
import random

# ===============================
# PARAMÈTRES DE LA MÉLODIE
# ===============================
tempo_bpm = 160                  # tempo en battements par minute
ticks_per_beat = 480              # résolution MIDI
note_duration = 480               # durée fixe (une noire = 1 beat)
nombre_mesures = 8                # longueur de la mélodie

# Gamme de DO majeur (notation MIDI : Do4 = 60)
gamme_do_majeur = [60, 62, 64, 65, 67, 69, 71, 72]

# ===============================
# CRÉATION DU FICHIER MIDI
# ===============================
mid = MidiFile(ticks_per_beat=ticks_per_beat)
track = MidiTrack()
mid.tracks.append(track)

# Ajout du tempo
track.append(Message('program_change', program=0, time=0))  # Instrument = Piano
track.append(MetaMessage('set_tempo', tempo=bpm2tempo(tempo_bpm)))

# ===============================
# GÉNÉRATION DE LA MÉLODIE
# ===============================
melodie = []
note_actuelle = random.choice(gamme_do_majeur)  # point de départ

for mesure in range(nombre_mesures):
    for beat in range(4):  # 4 temps par mesure
        # Règle 1 : rester dans la gamme
        note_candidats = gamme_do_majeur
        
        # Règle 2 : mouvement conjoint privilégié (éviter grands sauts)
        voisins = [n for n in note_candidats if abs(n - note_actuelle) <= 4]
        
        # Règle 3 : éviter trop de répétitions
        if melodie[-2:] == [note_actuelle, note_actuelle]:
            voisins = [n for n in voisins if n != note_actuelle]
        
        # Choix de la prochaine note
        if voisins:
            note_suivante = random.choice(voisins)
        else:
            note_suivante = random.choice(note_candidats)
        
        melodie.append(note_suivante)
        note_actuelle = note_suivante

# ===============================
# ÉCRITURE DES NOTES DANS LE MIDI
# ===============================
for note in melodie:
    track.append(Message('note_on', note=note, velocity=80, time=0))
    track.append(Message('note_off', note=note, velocity=80, time=note_duration))

# Sauvegarde
mid.save("melodie_do_majeur.mid")

print("✅ Fichier 'melodie_do_majeur.mid' créé avec succès !")
