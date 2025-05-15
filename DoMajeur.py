import numpy as np
import sounddevice as sd
import time  # Pour ajouter une pause

# Paramètres
notes = [261.63, 293.66, 329.63, 349.23, 392.00, 440.00, 493.88, 523.25]  # Do-Ré-Mi-Fa-Sol-La-Si-Do
durée = 0.5  # Durée par note (secondes)
pause = 0.1  # Pause entre les notes (secondes)
échantillonnage = 44100  # Hz

# Jouer chaque note avec fade-in/fade-out et une courte pause
for fréquence in notes:
    t = np.linspace(0, durée, int(échantillonnage * durée), endpoint=False)
    signal = np.sin(2 * np.pi * fréquence * t)
    
    # Fade-in / Fade-out
    fade_in = np.linspace(0, 1, int(len(signal) * 0.2))
    fade_out = np.linspace(1, 0, int(len(signal) * 0.2))
    signal[:len(fade_in)] *= fade_in
    signal[-len(fade_out):] *= fade_out
    
    sd.play(signal, échantillonnage)
    sd.wait()  # Attendre la fin de la note
    
    time.sleep(pause)  # Ajout d'un petit silence entre les notes
