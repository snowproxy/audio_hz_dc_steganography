import numpy as np
import scipy.io.wavfile as wav
from scipy.fft import fft
from pydub import AudioSegment
import base64

char_to_hz = {char: i*400 for i, char in enumerate(' abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789+/.,;:!?"()-\'')}
hz_to_char = {i: char for char, i in char_to_hz.items()}

def text_to_audio(text, filename):
    hzs = [char_to_hz.get(char, 0) for char in text]
    rate = 44100
    T = 0.005
    t = np.linspace(0, T, int(T*rate), False)
    audio_data = np.array([])

    for hz in hzs:
        freq = hz
        sample = 0.5 * np.sin(2 * np.pi * freq * t)
        audio_data = np.append(audio_data, sample)

    audio_data *= 32767 / np.max(np.abs(audio_data))
    audio_data = audio_data.astype(np.int16)
    wav.write(filename + '.wav', rate, audio_data)

    audio = AudioSegment.from_wav(filename + '.wav')
    audio.export(filename + '.mp3', format="mp3")

def audio_to_text(filename):
    rate, data = wav.read(filename + '.wav')
    T = 0.005
    samples_per_chunk = int(T * rate)
    chunks = np.array([data[i:i+samples_per_chunk] for i in range(0, len(data), samples_per_chunk)])

    text = ''

    for chunk in chunks:
        chunk_fft = fft(chunk)
        dominant_freq_index = np.argmax(np.abs(chunk_fft))
        dominant_freq = rate * dominant_freq_index / len(chunk)
        print(f"Dominant frequency: {dominant_freq} Hz")
        hz = round(dominant_freq / 400) * 400 
        print(f"Hz value: {hz}")
        text += hz_to_char.get(hz, '?')

    return text

def decode():
    z = audio_to_text('encoded')
    print(f"decoded text: {z}")

def encode():
    text_to_audio('enter your text here to be encoded, alternatively you can input a base64 string of a file to encode that instead, note this will take a while as this script is not funny optimized.', 'encoded')
    


#decode()
encode()
