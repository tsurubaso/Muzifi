from mido import MidiFile, MidiTrack, Message

scales = {
    "C_major__A_minor":      [60, 62, 64, 65, 67, 69, 71, 72],  # C D E F G A B C
    "G_major__E_minor":      [67, 69, 71, 72, 74, 76, 78, 79],  # G A B C D E F# G
    "D_major__B_minor":      [62, 64, 66, 67, 69, 71, 73, 74],  # D E F# G A B C# D
    "A_major__Fsharp_minor":[69, 71, 73, 74, 76, 78, 80, 81],  # A B C# D E F# G# A
    "F_major__D_minor":      [65, 67, 69, 70, 72, 74, 76, 77],  # F G A Bb C D E F
    "Bb_major__G_minor":     [70, 72, 74, 75, 77, 79, 81, 82],  # Bb C D Eb F G A Bb
    "Eb_major__C_minor":     [63, 65, 67, 68, 70, 72, 74, 75],  # Eb F G Ab Bb C D Eb
}

for name, notes in scales.items():
    mid = MidiFile()
    track = MidiTrack()
    mid.tracks.append(track)

    track.append(Message('program_change', program=0, time=0))  # Piano

    for note in notes:
        track.append(Message('note_on', note=note, velocity=64, time=0))
        track.append(Message('note_off', note=note, velocity=64, time=480))

    mid.save(f"{name}.mid")
    print(f"✅ Fichier : {name}.mid")
