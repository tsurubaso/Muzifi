import numpy as np
import sounddevice as sd
import time

# Notes de la gamme pentatonique majeure de Do (fréquences en Hz)
notes = [261.63, 293.66, 329.63, 392.00, 440.00]  # Do - Ré - Mi - Sol - La
durée = 0.5  # Durée par note (secondes)
pause = 0.1  # Pause entre les notes (secondes)
échantillonnage = 44100  # Hz

# Jouer chaque note avec un fade-in / fade-out et une courte pause
for fréquence in notes:
    t = np.linspace(0, durée, int(échantillonnage * durée), endpoint=False)
    signal = np.sin(2 * np.pi * fréquence * t)

    # Appliquer un fade-in / fade-out
    fade_in = np.linspace(0, 1, int(len(signal) * 0.2))
    fade_out = np.linspace(1, 0, int(len(signal) * 0.2))
    signal[:len(fade_in)] *= fade_in
    signal[-len(fade_out):] *= fade_out

    sd.play(signal, échantillonnage)
    sd.wait()
    time.sleep(pause)  # Ajout d'une courte pause
