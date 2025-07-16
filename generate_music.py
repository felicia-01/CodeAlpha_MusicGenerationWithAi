from music21 import stream, note, chord, tempo, instrument
from tensorflow.keras.models import load_model
import numpy as np
import pickle
from fractions import Fraction

def generate_music(style, seconds=30, filename="output.mid", temperature=1.0):
    # Load model and mappings from Google Drive
    model = load_model(f"/content/drive/MyDrive/{style}_model.h5", compile=False)
    with open(f"/content/drive/MyDrive/{style}_note_to_int.pkl", "rb") as f:
        note_to_int = pickle.load(f)
    with open(f"/content/drive/MyDrive/{style}_notes.pkl", "rb") as f:
        notes = pickle.load(f)

    int_to_note = {i: n for n, i in note_to_int.items()}
    n_vocab = len(note_to_int)

    seed = notes[:50]
    pattern = [note_to_int[n] for n in seed]
    output_notes = []

    total_time_beats = 0
    max_beats = seconds * 2  # Assuming 120 BPM = 2 beats/sec

    def sample(preds, temperature=1.0):
        preds = np.asarray(preds).astype('float64')
        preds = np.log(preds + 1e-9) / temperature
        exp_preds = np.exp(preds)
        preds = exp_preds / np.sum(exp_preds)
        probas = np.random.multinomial(1, preds, 1)
        return np.argmax(probas)

    while total_time_beats < max_beats:
        input_seq = np.reshape(pattern[-50:], (1, 50, 1)) / float(n_vocab)
        preds = model.predict(input_seq, verbose=0)[0]
        index = sample(preds, temperature)
        result = int_to_note[index]

        if "_" not in result:
            continue

        parts = result.split("_")
        if len(parts) < 4:
            continue

        pitch, duration, velocity, instr = parts

        try:
            dur = float(Fraction(duration))
        except:
            dur = 0.25

        # 🔸 Style-specific behavior
        if style == "jazz":
            dur = max(0.25, dur * np.random.uniform(0.5, 1.0))
            velocity = min(127, int(velocity) + np.random.randint(10, 30))
        elif style == "classical":
            dur = dur * np.random.uniform(1.0, 2.0)
            velocity = max(30, int(velocity) - np.random.randint(0, 20))
        elif style == "calm":
            if "." not in pitch and pitch[-1].isdigit():
                octave = int(pitch[-1])
                if octave > 5:
                    continue  # Skip high-pitched notes

        total_time_beats += dur

        # 🎼 Create the Note or Chord
        if "." in pitch:
            try:
                chord_notes = [int(p) for p in pitch.split(".")]
                output_notes.append(chord.Chord(chord_notes, quarterLength=dur))
            except:
                continue
        else:
            try:
                output_notes.append(note.Note(pitch, quarterLength=dur))
            except:
                continue

        pattern.append(index)

    # 🎵 Build MIDI stream with appropriate instrument
    midi_stream = stream.Stream()
    midi_stream.append(tempo.MetronomeMark(number=120))

    # 🧠 Assign style-based instrument
    if style == "jazz":
        midi_stream.append(instrument.Trumpet())  # or instrument.ElectricPiano()
    elif style == "classical":
        midi_stream.append(instrument.Flute())  # or instrument.PadSynth()
    elif style == "calm":
        midi_stream.append(instrument.Guitar())  # or instrument.StringEnsemble()

    for n in output_notes:
        midi_stream.append(n)

    midi_stream.write("midi", fp=filename)
    print(f"✅ Music generated: {filename}")
