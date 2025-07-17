## CodeAlpha_MusicGenerationWithAi
An interactive AI-powered music generator that composes short melodies in Jazz, Classical, or Calm styles using MIDI files and LSTM neural networks.

### Features
-  **Multiple Styles:** Supports **Jazz**, **Classical**, and **Calm** music generation.
-  **Deep Learning Models:** LSTM-based RNN trained on parsed MIDI files.
-  **Interactive UI:** Easily select music style and duration via widgets (Google Colab).
-  **Audio Playback:** Converts generated MIDI to MP3 using **FluidSynth** and **pydub** for seamless playback.
-  **Google Drive Integration:** Save and reuse trained models without retraining.
-  **Playback Speed Control:** Easily adjust the tempo of generated music (120 BPM by default).
-  **Downloadable Output:** Automatically saves generated MIDI and MP3 files for offline use.
-  **Sound-Enriched Output:** Captures expressive musicality with pitch, velocity, duration, and basic instrument assignment.

### Project Objectives
- Collect MIDI music data to train your AI model (classical, jazz etc.).
- Preprocess the data into note sequences suitable for training (e.g., using `music21`).
- Build a deep learning model using RNNs like LSTM to learn music patterns.
- Train the model on the dataset to generate new music sequences.
- Convert generated sequences to MIDI and play or save them as audio.

### How It Works
**Preprocess MIDI using music21** to extract pitch, duration, velocity, and instrument, then store as note sequences (.pkl format).
**Train an LSTM model** on these sequences (50-note windows) and save .h5 models with mappings.
**Generate music** using the model with style-specific rules, convert MIDI to MP3 using FluidSynth + Pydub, and play the result.

### Workflow   
All the required code—parsing, training, generating, conversion, and interactive GUI—is included in this repository. Simply follow the steps below to run everything inside Google Colab

**Install Dependencies**
!pip install music21 tensorflow pydub
!apt-get install -y fluidsynth ffmpeg

**Upload MIDI Files to Colab**
Upload your .mid files (for Jazz, Classical, and Calm) to your Colab workspace.

**Mount Google Drive**
Save all parsed data and trained models directly to Google Drive to avoid retraining every time.

from google.colab import drive
drive.mount('/content/drive')

**Start the program:**
After mounting Google Drive, parse the uploaded MIDI files, then train LSTM models for each style. Once trained, generate new music using the models, convert it to MP3, and play it interactively through the GUI.


### Output:

<img width="350" height="175" alt="image" src="https://github.com/user-attachments/assets/12fb7335-0175-4719-a985-b43e834ae0d4" />
<img width="350" height="304" alt="image" src="https://github.com/user-attachments/assets/a97cd2b4-ed17-430c-8dec-c1f343d5acf9" />
<img width="254" height="185" alt="output_music" src="https://github.com/user-attachments/assets/456b6b0a-e3bc-43b1-99b0-2822a165be50" />


