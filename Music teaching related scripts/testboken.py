from bokeh.plotting import figure, show
from bokeh.models import ColumnDataSource, LabelSet
import pretty_midi
import numpy as np
import os

european_notes = ['Do', 'Do#', 'Ré', 'Ré#', 'Mi', 'Fa', 'Fa#', 'Sol', 'Sol#', 'La', 'La#', 'Si']

def detect_chord_name(pitches):
    if len(pitches) < 3:
        return "N/A"
    pitch_classes = sorted(set([p % 12 for p in pitches]))
    for root in range(12):
        maj = sorted([(root + i) % 12 for i in [0, 4, 7]])
        min_ = sorted([(root + i) % 12 for i in [0, 3, 7]])
        if pitch_classes == maj:
            return european_notes[root] + " majeur"
        if pitch_classes == min_:
            return european_notes[root] + " mineur"
    return "Autre"

def extract_chords_from_midi(midi_file_path):
    midi_data = pretty_midi.PrettyMIDI(midi_file_path)
    chords = []
    for instrument in midi_data.instruments:
        notes = sorted(instrument.notes, key=lambda n: n.start)
        current_chord = []
        for note in notes:
            if current_chord and note.start - current_chord[-1].end > 0.1:
                chords.append([n.pitch for n in current_chord])
                current_chord = []
            current_chord.append(note)
        if current_chord:
            chords.append([n.pitch for n in current_chord])
    return chords

def compute_tonnetz(chords):
    tonnetz_points = []
    labels = []
    for chord in chords:
        if len(chord) < 3:
            continue
        pitches = sorted(chord[:3])
        i1 = pitches[1] - pitches[0]
        i2 = pitches[2] - pitches[0]
        i3 = pitches[2] - pitches[1]
        T1 = i1 - i2
        T2 = i1 - i3
        T3 = i2 - i3
        tonnetz_points.append([T1, T2, T3])
        labels.append(detect_chord_name(pitches))
    return np.array(tonnetz_points), labels

def create_tonnetz_chart():
    p = figure(title="Tonnetz enrichi avec noms d'accords",
               x_axis_label='Fondamentale - Tierce',
               y_axis_label='Fondamentale - Quinte',
               width=800, height=800)
    p.patch([0, 1, 0], [0, 0, 1], color="lightgray", alpha=0.4, legend_label="Accords majeurs")
    p.patch([0, -1, 0], [0, 0, -1], color="lightgray", alpha=0.4, legend_label="Accords mineurs")
    p.grid.grid_line_alpha = 0.3
    return p

def plot_tonnetz_with_chart(tonnetz_points, labels):
    p = create_tonnetz_chart()
    source = ColumnDataSource(data=dict(
        x=tonnetz_points[:, 0],
        y=tonnetz_points[:, 1],
        size=[6]*len(tonnetz_points),
        color=['blue']*len(tonnetz_points),
        label=labels,
    ))
    p.scatter(x='x', y='y', size='size', color='color', source=source)
    label_set = LabelSet(x='x', y='y', text='label', x_offset=5, y_offset=5,
                     source=source)

    p.add_layout(label_set)
    show(p)

def main():
    midi_file_path = input("Entrez le chemin du fichier MIDI : ").strip('"')
    if not os.path.exists(midi_file_path):
        print("Fichier introuvable :", midi_file_path)
        return
    chords = extract_chords_from_midi(midi_file_path)
    tonnetz_points, labels = compute_tonnetz(chords)
    if len(tonnetz_points) == 0:
        print("Aucun accord valide trouvé.")
        return
    plot_tonnetz_with_chart(tonnetz_points, labels)

if __name__ == "__main__":
    main()
