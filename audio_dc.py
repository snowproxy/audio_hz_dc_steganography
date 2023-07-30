import numpy as np
import scipy.io.wavfile as wav
from scipy.fft import fft
from pydub import AudioSegment

char_to_db = {char: i for i, char in enumerate('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789 .,;:!?"()-\'')}

db_to_char = {i: char for char, i in char_to_db.items()}

def text_to_audio(text, filename):
    dbs = [char_to_db.get(char, 0) for char in text]
    rate = 44100
    T = 0.1
    t = np.linspace(0, T, int(T*rate), False)
    audio_data = np.array([])

    for db in dbs:
        freq = 440 * 2**(db/12)
        sample = 0.5 * np.sin(2 * np.pi * freq * t)
        audio_data = np.append(audio_data, sample)

    audio_data *= 32767 / np.max(np.abs(audio_data))
    audio_data = audio_data.astype(np.int16)
    wav.write(filename + '.wav', rate, audio_data)

    audio = AudioSegment.from_wav(filename + '.wav')
    audio.export(filename + '.mp3', format="mp3")

def audio_to_text(filename):
    rate, data = wav.read(filename + '.wav')
    T = 0.1
    samples_per_chunk = int(T * rate)
    chunks = np.array([data[i:i+samples_per_chunk] for i in range(0, len(data), samples_per_chunk)])

    text = ''

    for chunk in chunks:
        chunk_fft = fft(chunk)
        dominant_freq_index = np.argmax(np.abs(chunk_fft))
        dominant_freq = rate * dominant_freq_index / len(chunk)
        print(f"Dominant frequency: {dominant_freq} Hz")
        db = round(12 * np.log2(dominant_freq / 440.0))
        print(f"Decibel value: {db}")
        text += db_to_char.get(db, '?')

    return text

def decode():
    print(audio_to_text('encoded'))

def encode():
    text = "this is an example text, you can put whatever you want here as long as it is in the character dictionary at the top of the page"
    text_to_audio(text, 'encoded')

#decode()
encode()