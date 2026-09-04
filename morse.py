"""Small Morse encoder and decoder used by Coxor."""

import re

MORSE_CODE = {
    "A": ".-", "B": "-...", "C": "-.-.", "D": "-..", "E": ".", "F": "..-.",
    "G": "--.", "H": "....", "I": "..", "J": ".---", "K": "-.-", "L": ".-..",
    "M": "--", "N": "-.", "O": "---", "P": ".--.", "Q": "--.-", "R": ".-.",
    "S": "...", "T": "-", "U": "..-", "V": "...-", "W": ".--", "X": "-..-",
    "Y": "-.--", "Z": "--..",
    "0": "-----", "1": ".----", "2": "..---", "3": "...--", "4": "....-",
    "5": ".....", "6": "-....", "7": "--...", "8": "---..", "9": "----.",
    "?": "..--..",
}

REVERSE_MORSE = {code: character for character, code in MORSE_CODE.items()}


def text_to_morse(text: str) -> str:
    """Convert supported text to Morse; unsupported characters become '?'."""
    if not text.strip():
        return ""
    words = []
    for word in re.split(r"\s+", text.strip().upper()):
        symbols = [MORSE_CODE.get(character, "?") for character in word]
        words.append(" ".join(symbols))
    return " / ".join(words)


def morse_to_text(morse: str) -> str:
    """Decode slash-separated words and space-separated letters."""
    decoded_words = []
    for word in morse.split("/"):
        letters = []
        for symbol in word.strip().split():
            letters.append(REVERSE_MORSE.get(symbol, "?"))
        decoded_words.append("".join(letters))
    return " ".join(decoded_words).strip()
