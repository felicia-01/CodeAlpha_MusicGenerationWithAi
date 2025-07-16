from pydub import AudioSegment
import subprocess
from IPython.display import Audio, display

def convert_and_play(mid_file):
    wav_file = mid_file.replace(".mid", ".wav")
    mp3_file = mid_file.replace(".mid", ".mp3")

    soundfont_path = "/usr/share/sounds/sf2/FluidR3_GM.sf2"

    # Convert MIDI to WAV using FluidSynth
    subprocess.run(["fluidsynth", "-ni", soundfont_path, mid_file, "-F", wav_file, "-r", "44100"], check=True)

    # Convert WAV to MP3
    sound = AudioSegment.from_wav(wav_file)
    sound.export(mp3_file, format="mp3")

    display(Audio(mp3_file))
    print(f"▶️ Playing: {mp3_file}")
