#SPDX-FileCopyrightText: 2026 Josué Enrique Barredo Alamilla
#SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0

# This decides what runs each time and when.
# After settings are implemented, this will read from there and call whichever and however they apply

from dotenv import load_dotenv
load_dotenv()
import translator
import voiceover
import extractor

# this is what passes for I/O config rn
l1 = "es"
l2 = None
# This, is a quick sample text for testing translations and text-to-speech--Do I sound good?
def main():
    l2_text = extractor.clipboard_extract()
    l1_text = translator.lara_translate(l1 = l1, l2 = l2, l2_text = l2_text)
    voiceover.fish_voiceover(l2_text)

if __name__ == "__main__":
    main()
