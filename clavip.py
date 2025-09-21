import pygame

from mido import MidiFile, MidiTrack, Message
import time

# ───────────────
# CONFIG
# ───────────────
BASE_OCTAVE = 4
TICKS_PER_BEAT = 480

KEY_TO_NOTE = {
    'a': 0, 's': 2, 'd': 4, 'f': 5, 'g': 7, 'h': 9, 'j': 11,
    'w': 1, 'e': 3, 't': 6, 'y': 8, 'u': 10,
}

OCTAVE_UP = 'o'
OCTAVE_DOWN = 'p'

# ───────────────
# INIT
# ───────────────
pygame.init()
screen = pygame.display.set_mode((600, 200))
pygame.display.set_caption("Clavier MIDI QWERTY")

font = pygame.font.SysFont(None, 36)

midi_file = MidiFile()
track = MidiTrack()
midi_file.tracks.append(track)

pressed_notes = {}  # touche -> (note MIDI, timestamp)
current_octave = BASE_OCTAVE
running = True

# ───────────────
# LOOP
# ───────────────
while running:
    screen.fill((0, 0, 0))  # fond noir
    
    # Affichage des touches pressées
    text_pressed = "Notes: " + " ".join(pressed_notes.keys())
    img_pressed = font.render(text_pressed, True, (255, 255, 255))
    screen.blit(img_pressed, (20, 50))
    
    # Affichage de l'octave
    img_octave = font.render(f"Octave: {current_octave}", True, (255, 255, 0))
    screen.blit(img_octave, (20, 100))
    
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            key = pygame.key.name(event.key).lower()
            if key in KEY_TO_NOTE and key not in pressed_notes:
                midi_note = KEY_TO_NOTE[key] + current_octave * 12
                pressed_notes[key] = (midi_note, time.time())
                track.append(Message('note_on', note=midi_note, velocity=64, time=0))
            elif key == OCTAVE_UP:
                current_octave += 1
            elif key == OCTAVE_DOWN:
                current_octave -= 1

        elif event.type == pygame.KEYUP:
            key = pygame.key.name(event.key).lower()
            if key in pressed_notes:
                midi_note, start_time = pressed_notes.pop(key)
                duration = int((time.time() - start_time) * TICKS_PER_BEAT)
                track.append(Message('note_off', note=midi_note, velocity=64, time=duration))

# ───────────────
# SAVE MIDI
# ───────────────
pygame.quit()
midi_file.save("ma_musique_qwerty.mid")
print("MIDI sauvegardé : ma_musique_qwerty.mid")
