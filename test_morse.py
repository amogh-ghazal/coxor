import unittest

from morse import morse_to_text, text_to_morse


class MorseTests(unittest.TestCase):
    def test_text_to_morse(self):
        self.assertEqual(text_to_morse("SOS 42"), "... --- ... / ....- ..---")

    def test_round_trip(self):
        original = "HELLO 2026"
        self.assertEqual(morse_to_text(text_to_morse(original)), original)

    def test_unsupported_character(self):
        self.assertEqual(morse_to_text(text_to_morse("HI!")), "HI?")

    def test_extra_spaces_are_normalized(self):
        self.assertEqual(morse_to_text(text_to_morse("HI   42")), "HI 42")


if __name__ == "__main__":
    unittest.main()
