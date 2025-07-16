import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from tensorflow.keras.utils import to_categorical
import pickle

styles = list(style_keywords.keys())
sequence_length = 50

for style in styles:
    print(f"\nTraining model for: {style}")

    # Load notes for the style
    with open(f"{style}_notes.pkl", "rb") as f:
        notes = pickle.load(f)

    # Create mappings
    unique_notes = sorted(set(notes))
    note_to_int = {note: i for i, note in enumerate(unique_notes)}

    # Prepare sequences
    X = []
    y = []
    for i in range(len(notes) - sequence_length):
        seq_in = notes[i:i + sequence_length]
        seq_out = notes[i + sequence_length]
        X.append([note_to_int[n] for n in seq_in])
        y.append(note_to_int[seq_out])

    n_vocab = len(unique_notes)
    X = np.reshape(X, (len(X), sequence_length, 1)) / float(n_vocab)
    y = to_categorical(y, num_classes=n_vocab)

    # Define LSTM model
    model = Sequential([
        LSTM(256, input_shape=(X.shape[1], X.shape[2]), return_sequences=True),
        Dropout(0.3),
        LSTM(256),
        Dense(256, activation='relu'),
        Dense(n_vocab, activation='softmax')
    ])

    model.compile(loss='categorical_crossentropy', optimizer='adam')

    # Train model
    model.fit(X, y, epochs=30, batch_size=64)
    print(f"✅ Trained model for {style}")

    # Save model and mappings to Google Drive
    model.save(f"/content/drive/MyDrive/{style}_model.h5")
    with open(f"/content/drive/MyDrive/{style}_note_to_int.pkl", "wb") as f:
        pickle.dump(note_to_int, f)
    with open(f"/content/drive/MyDrive/{style}_notes.pkl", "wb") as f:
        pickle.dump(notes, f)
