import glob, pickle, os
from music21 import converter, note, chord
from collections import defaultdict

# Fix possible double .mid.mid extensions
for f in glob.glob("*.mid.mid"):
    os.rename(f, f.replace(".mid.mid", ".mid"))

style_keywords = {
    'jazz': 'jazz',
    'classical': 'class',
    'calm': 'calm'
}

style_notes = defaultdict(list)

for style, keyword in style_keywords.items():
    files = [f for f in glob.glob("*.mid") if keyword in f.lower()]
    for file in files:
        try:
            midi = converter.parse(file)
            for el in midi.flatten().notes:
                try:
                    duration = el.quarterLength
                    velocity = el.volume.velocity if el.volume.velocity else 64  # default velocity
                    instrument = el.getInstrument(returnDefault=True).instrumentName or "Unknown"

                    if isinstance(el, note.Note):
                        pitch = str(el.pitch)
                    elif isinstance(el, chord.Chord):
                        pitch = ".".join(str(n) for n in el.normalOrder)
                    else:
                        continue

                    note_str = f"{pitch}_{duration}_{velocity}_{instrument}"
                    style_notes[style].append(note_str)

                except Exception as e:
                    # Ignore problematic notes
                    pass
        except Exception as e:
            print(f"⚠️ Skipped {file}: {e}")

# Save parsed notes to .pkl for each style
for style in style_notes:
    with open(f"{style}_notes.pkl", "wb") as f:
        pickle.dump(style_notes[style], f)
print("✅ MIDI files parsed and saved.")
