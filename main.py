#SPDX-FileCopyrightText: 2026 Josué Enrique Barredo Alamilla
#SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0

import os, datetime, dotenv
import translators
import voiceovers
import extractors

# Это - простой тестовый фрагмент текста для проверки синтеза речи и перевода--звучу ли я приемлемо?
########## config #############
# Full explanation: https://developers.laratranslate.com/docs/supported-languages
# Short explanation: Strings of 2-letter codes for langs (ISO639) and regions (optional, prefixed with a dash: "es-MX", "fr-CA", "zh-CN")
user_l1 = "en"   # The language you understand
user_l2 = None   # The language you're learning--None auto-selects; 
ENABLE_INITIALIZATION_DOTFILES = True # Basic .env % .tmp check
###############################

# main() decides what runs and when.
def main():

    if ENABLE_INITIALIZATION_DOTFILES:
        initialize_dotfiles()

    l2_text = extractors.clipboard_extract()

    timestamp = generate_timestamp()

    if user_l2 == None:
        l1_text, identified_l2   = translators.lara_translate(raws = l2_text, lang_in = None, lang_out = user_l1)
    else:
        l1_text, _          = translators.lara_translate(raws = l2_text, lang_in = user_l2, lang_out = user_l1)

    if user_l2 == None:
        print(f"{identified_l2}: {l2_text}")
    else:
        print(f"{user_l2}: {l2_text}")    

    print(f"{user_l1}: {l1_text}")

    l2_audio = voiceovers.fish_voiceover(raws=l2_text)

    l2_audio_filename = "./.tmp/" + timestamp + ".mp3"
    with open(l2_audio_filename, "wb") as file:
        file.write(l2_audio)
    print(f"✓ Audio saved to {l2_audio_filename}")


def generate_timestamp():
    timestamp = datetime.datetime.now().strftime("%y-%m-%dT%H-%M-%S")
    return timestamp

def initialize_dotfiles():
    # Check if .env exists and, if it doesn't, fill up empty keys.
    if not os.path.isfile("./.env"):
        with open(".env", "w") as file:
            file.write("FISHAUDIO_API_KEY=\nFISHAUDIO_VOICE_ID=\nLARA_ACCESS_KEY_ID=\nLARA_ACCESS_KEY_SECRET=")
        print("Created a sample './.env' file to read API keys from")
    # Check if .tmp/ exists and, if it doesn't, create it
    if not os.path.isdir("./.tmp"):
        os.mkdir("./.tmp")
        print("Created a './.tmp' directory to dump outputs for testing")
    dotenv.load_dotenv()

if __name__ == "__main__":
    main()
