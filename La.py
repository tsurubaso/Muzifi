import numpy as np
import sounddevice as sd

# Paramètres du son
fréquence = 440  # La (A4)
durée = 2  # en secondes
échantillonnage = 44100  # Hz

# Génération du signal sinusoïdal
t = np.linspace(0, durée, int(échantillonnage * durée), endpoint=False)
signal = np.sin(2 * np.pi * fréquence * t)

# Lecture du son
sd.play(signal, échantillonnage)
sd.wait()
