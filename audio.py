"""Generate simple Morse WAV files without external audio libraries."""

import math
import struct
import wave
from pathlib import Path

FREQUENCY = 1000
SAMPLE_RATE = 44100
DOT_SECONDS = 0.150
DASH_SECONDS = 0.450
SYMBOL_GAP_SECONDS = 0.150
LETTER_GAP_SECONDS = 0.450
WORD_GAP_SECONDS = 1.050


def _silence(samples: list[int], seconds: float) -> None:
    samples.extend([0] * round(SAMPLE_RATE * seconds))


def _tone(samples: list[int], seconds: float) -> None:
    count = round(SAMPLE_RATE * seconds)
    amplitude = 12000
    for index in range(count):
        value = round(amplitude * math.sin(2 * math.pi * FREQUENCY * index / SAMPLE_RATE))
        samples.append(value)


def morse_to_samples(morse: str) -> list[int]:
    samples: list[int] = []
    words = morse.split("/")
    for word_index, word in enumerate(words):
        letters = word.strip().split()
        for letter_index, letter in enumerate(letters):
            for symbol_index, symbol in enumerate(letter):
                if symbol == ".":
                    _tone(samples, DOT_SECONDS)
                elif symbol == "-":
                    _tone(samples, DASH_SECONDS)
                else:
                    continue
                if symbol_index < len(letter) - 1:
                    _silence(samples, SYMBOL_GAP_SECONDS)
            if letter_index < len(letters) - 1:
                _silence(samples, LETTER_GAP_SECONDS)
        if word_index < len(words) - 1:
            _silence(samples, WORD_GAP_SECONDS)
    return samples


def write_wav(morse: str, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    samples = morse_to_samples(morse)
    with wave.open(str(output_path), "wb") as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(SAMPLE_RATE)
        wav_file.writeframes(b"".join(struct.pack("<h", sample) for sample in samples))
