#SPDX-FileCopyrightText: 2026 Josué Enrique Barredo Alamilla
#SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0

"""
Sombrita: Takes new text on the clipboard and generates translation and voiceover. You need to configure L1_CODE and L2_CODE.

Single shot. Per run:
    1.- Clipboard: Poll indefinitely for next text on clipboard (L2 fragment).
    2.- Translate: MT it into L1 with Lara Translate, auto-detecting if L2 is None (L1 fragment).
    3.- Voiceover: Get L2 voiceover with Fish Audio
    4.- Outputs: .mp3 gets dumped into ./.tmp/ while both text fragments get printed;
"""

import os, datetime
import dotenv
import extractors, translators, voiceovers

########## config #############
# IETF BCP 47 language tags: For practical purposes, a 2-char ISO 639
# optionally followed by a dash-prefixed region: ("es-MX", "fr-CA", "zh-CN").
# Full list of what Lara accepts: https://developers.laratranslate.com/docs/supported-languages
L1_CODE = "en"   # The language you understand
L2_CODE = None   # The language you're learning--None is "Auto"; 

ENABLE_INITIALIZATION_DOTFILES = True # Basic .env % .tmp check
###############################


# Normalize to lowercase lang, uppercase region: "ll-RR"
# From now on it is assumed that the leftmost 2-characters stand for the lang,
# the rightmost 2 for the region. If there's no region set, the normalization
# will create a real region I don't support (e.g. "es-ES"), a completely made up
# region ("zh-ZH"), or a real region I support (e.g. "ru-RU"), but that is okay,
# because these mistakes will all match their respective default locale.
if L2_CODE is not None:
    L2_CODE = L2_CODE[:2].lower() + "-" + L2_CODE[-2:].upper()
L1_CODE = L1_CODE[:2].lower() + "-" + L1_CODE[-2:].upper()


def main():
    """
    Doesn't loop, so it receives one text fragment and writes one .mp3.

    Blocks until new text is found on the clipboard. Doesn't return anything
    """

    if ENABLE_INITIALIZATION_DOTFILES:
        initialize_dotfiles()

    l2_text = extractors.clipboard_extract()

    timestamp = generate_timestamp()

    if L2_CODE is None:
        # Let translator auto-detect the source language, then hand the detected
        # code to the voiceover so the voice matches the actual L2.
        l1_text, identified_l2_code  = translators.lara_translate(raws = l2_text, lang_in = None, lang_out = L1_CODE)
        print(f"{identified_l2_code}: {l2_text}")
        l2_audio = voiceovers.fish_voiceover(raws=l2_text, lang_in=identified_l2_code)
    else:
        l1_text, _ = translators.lara_translate(raws = l2_text, lang_in = L2_CODE, lang_out = L1_CODE)
        print(f"{L2_CODE}: {l2_text}")
        l2_audio = voiceovers.fish_voiceover(raws=l2_text, lang_in=L2_CODE)

    l2_audio_filename = "./.tmp/" + timestamp + ".mp3"
    with open(l2_audio_filename, "wb") as file:
        file.write(l2_audio)
    print(f"{L1_CODE}: {l1_text}")   
    print(f"✓ Audio saved to {l2_audio_filename}")


def generate_timestamp():
    """Filename-friendly, ISO-like, local timestamp (e.g. '26-09-23T08-52-39')."""
    timestamp = datetime.datetime.now().strftime("%y-%m-%dT%H-%M-%S")
    return timestamp

def initialize_dotfiles():
    """Create a template .env and the .tmp/ dumping dir if they're missing."""
# Check if .env exists and, if it doesn't, fill up empty keys.
    if not os.path.isfile("./.env"):
        with open(".env", "w") as file:
            file.write("LARA_ACCESS_KEY_ID=\nLARA_ACCESS_KEY_SECRET=\nFISH_API_KEY=\n")
        print("Created a sample './.env' file to read API keys from")
# Check if .tmp/ exists and, if it doesn't, create it
    if not os.path.isdir("./.tmp"):
        os.mkdir("./.tmp")
        print("Created a './.tmp' directory to dump outputs for testing")
    dotenv.load_dotenv()

if __name__ == "__main__":
    main()
