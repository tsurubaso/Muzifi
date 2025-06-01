import requests
import pretty_midi
import numpy as np
import matplotlib.pyplot as plt
import os

def download_midi(url, save_path):
    # Télécharger le fichier MIDI depuis l'URL
    response = requests.get(url)
    if response.status_code == 200:
        with open(save_path, 'wb') as f:
            f.write(response.content)
        print(f"Fichier téléchargé et sauvegardé sous : {save_path}")
    else:
        print("Erreur lors du téléchargement du fichier.")
        return None
    return save_path

def compute_tonnetz(chords):
    tonnetz_points = []

    for chord_ in chords:
        if len(chord_) < 3:
            continue  # Si l'accord a moins de 3 notes, on l'ignore

        # Extraire les trois premières notes (en MIDI)
        pitches = sorted([note for note in chord_])

        # Calculer les différences d'intervalles
        i1 = pitches[1] - pitches[0]
        i2 = pitches[2] - pitches[0]
        i3 = pitches[2] - pitches[1]
        
        # Calculer les coordonnées du Tonnetz
        T1 = i1 - i2  # Premier Tonnetz: distance entre la fondamentale et la tierce
        T2 = i1 - i3  # Deuxième Tonnetz: distance entre la fondamentale et la quinte
        T3 = i2 - i3  # Troisième Tonnetz: distance entre la tierce et la quinte
        
        tonnetz_points.append([T1, T2, T3])

    return np.array(tonnetz_points)

def plot_tonnetz(tonnetz_points):
    # Visualisation en 2D des 3 premières dimensions du Tonnetz
    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111)
    ax.plot(tonnetz_points[:, 0], tonnetz_points[:, 1], marker='o', markersize=5, linestyle='-', color='b')
    
    ax.set_xlabel('Dimension 1: Fondamentale - Tierce')
    ax.set_ylabel('Dimension 2: Fondamentale - Quinte')
    ax.set_title('Graphique du Tonnetz')

    plt.show()

def extract_chords_from_midi(midi_file_path):
    midi_data = pretty_midi.PrettyMIDI(midi_file_path)

    # On extrait les accords
    chords = []
    
    for instrument in midi_data.instruments:
        # Récupérer les notes de chaque instrument
        notes = [note for note in instrument.notes]
        
        # Groupement des notes en accords, ici on regroupe en utilisant une durée seuil
        current_chord = []
        for note in notes:
            if len(current_chord) > 0 and note.start - current_chord[-1].end > 0.1:
                # Si la différence de temps entre la note et la dernière est trop grande, on enregistre l'accord
                chords.append([n.pitch for n in current_chord])
                current_chord = []
            current_chord.append(note)
        
        # Ajouter le dernier accord
        if current_chord:
            chords.append([n.pitch for n in current_chord])

    return chords

def main():
    midi_file_path = input("Veuillez entrer le chemin local vers votre fichier MIDI : ").strip('"')
    
    # Vérifie que le fichier existe
    import os
    if not os.path.exists(midi_file_path):
        print("Fichier introuvable :", midi_file_path)
        return

    # Charger le fichier MIDI et extraire les accords
    chords = extract_chords_from_midi(midi_file_path)

    # Calculer les points du Tonnetz
    tonnetz_points = compute_tonnetz(chords)

    # Tracer le graphique du Tonnetz
    plot_tonnetz(tonnetz_points)

if __name__ == "__main__":
    main()
