#SPDX-FileCopyrightText: 2026 Josué Enrique Barredo Alamilla
#SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0

"""
Sombrita: Takes new text on the clipboard. Generates translation, voiceover. You need to config L1_CODE and L2_CODE

Single shot. Per run:
    1.- Clipboard: Poll indefinitely for next text on clipboard (L2 fragment).
    2.- Translate: MT it into L1 with Lara Translate, auto-detecting if L2 is None (L1 fragment).
    3.- Voiceover: Get L2 voiceover with Fish Audio
    4.- Outputs: .mp3 gets dumped into ./.tmp/ while both text fragments get printed;
"""

import datetime, os, sqlite3
import dotenv
import extractors, translators, voiceovers

########## config constants #############
# IETF BCP 47 language tags: For practical purposes, a 2-char ISO 639
# optionally followed by a dash-prefixed region: ("es-MX", "fr-CA", "zh-CN").
# Full list of what Lara accepts: https://developers.laratranslate.com/docs/supported-languages
LAN1_IDENTIFIER = "es" # The language you understand
REG1_IDENTIFIER = "MX" # L1's region code
LAN2_IDENTIFIER = "en" # Type None to auto-detect the language you're learning, but overrides USE_LOCAL_MT
REG2_IDENTIFIER = "GB" # L2's region code

USE_LOCAL_MT = False # True or False, but gets overridden if LAN2_IDENTIFIER = None
USE_LOCAL_TTS = True # True or False

ENABLE_INITIALIZATION_DOTFILES = True # Basic .env % .tmp check
#########################################

def main():
    """
    Doesn't loop, so it receives one text fragment and writes one .mp3.

    Blocks until new text is found on the clipboard. Doesn't return anything
    """

    if ENABLE_INITIALIZATION_DOTFILES:
        initialize_dotfiles()

    connection = sqlite3.connect("./.tmp/backlog.db")
    cursor = connection.cursor()
#    cursor.executescript()

    l1_code = make_locale_code(LAN1_IDENTIFIER, REG1_IDENTIFIER)
    if l1_code is None:
        print("Invalid L1_CODE, exiting")
        return
    l2_code = make_locale_code(LAN2_IDENTIFIER, REG2_IDENTIFIER)

    l2_text = extractors.clipboard_extract()

    timestamp = generate_timestamp()

    if l2_code is None:
        # Let translator auto-detect the source language, then hand the detected
        # code to the voiceover so the voice matches the actual L2.
        l1_text, identified_l2_code  = translators.lara_translate(raws = l2_text, lang_in = None, lang_out = l1_code)
        print(f"{identified_l2_code}: {l2_text}")
        l2_audio, ext = voiceovers.fish_voiceover(raws=l2_text, lang_in=identified_l2_code)
    elif not USE_LOCAL_MT and USE_LOCAL_TTS and l2_code == "en-GB":
        l1_text, identified_l2_code = translators.lara_translate(raws=l2_text, lang_in=l2_code, lang_out=l1_code)
        print(f"{l2_code}: {l2_text}")
        l2_audio, ext = voiceovers.kittentts_voiceover(raws=l2_text)
    elif USE_LOCAL_MT and not USE_LOCAL_TTS and l2_code == "ru-RU" and l1_code == "en-GB":
        l1_text = translators.translate_opus_mt_ru_to_en(l2_text)
        print(f"{l2_code}: {l2_text}")
        l2_audio, ext = voiceovers.fish_voiceover(raws=l2_text, lang_in=l2_code)
    else:
        l1_text, _ = translators.lara_translate(raws = l2_text, lang_in = l2_code, lang_out = l1_code)
        print(f"{l2_code}: {l2_text}")
        l2_audio, ext = voiceovers.fish_voiceover(raws=l2_text, lang_in=l2_code)

    l2_audio_filename = "./.tmp/" + timestamp + ext
    with open(l2_audio_filename, "wb") as file:
        file.write(l2_audio)
    print(f"{l1_code}: {l1_text}")
    print(f"✓ Audio saved to {l2_audio_filename}")

def make_locale_code(language, region):
    # "ll-RR". strip first, then normalize cases and slice. We assume the leftmost 2-chars are meaningful to guardrail
    # against SOME mistakes, e.g. ll = ' español ' and rr =' RUSSIA' both map to the intended identifiers.
    match (language, region):
        case (None, _) | ("", _):
            locale_code = None
        case (_, None) | (_, ""): # there is a lang identifier but no region, just duplicate lang identifier
            locale_code = language.strip()[:2].lower() + "-" + language.strip()[:2].upper()
        case (_, _):
            locale_code = language.strip()[:2].lower() + "-" + region.strip()[:2].upper()
    return locale_code

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
