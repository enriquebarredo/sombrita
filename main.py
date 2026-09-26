#SPDX-FileCopyrightText: 2026 Josué Enrique Barredo Alamilla
#SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0

import os, datetime, dotenv
import translators
import voiceovers
import extractors

# Это - простой тестовый фрагмент текста для проверки синтеза речи и перевода--звучу ли я приемлемо?
# このサーバーのチャンネルは上記のとおりです.
"""
'Twas brillig, and the slithy toves
      Did gyre and gimble in the wabe:
All mimsy were the borogoves,
      And the mome raths outgrabe.

“Beware the Jabberwock, my son!
      The jaws that bite, the claws that catch!
Beware the Jubjub bird, and shun
      The frumious Bandersnatch!” 
"""
# 為啥有這麼多人去點這個阿……? # taiwanese accent is really stronk holy guacamole what is that
# 城市会感到窒息,我只有寒冷。
# «Quand je bois, je pense--et quand je pense, je bois».
# can't get the tags to work, might be worthwhile to check
"""
[whispering] Lo cierto es que vivimos postergando todo lo postergable;
tal vez todos sabemos profundamente que somos inmortales y que tarde o temprano, 
todo hombre hará todas las cosas y sabrá todo.
"""

########## config #############
# Full explanation: https://developers.laratranslate.com/docs/supported-languages
# Short explanation: Strings of 2-letter codes for langs (ISO639) and regions (optional, prefixed with a dash: "es-MX", "fr-CA", "zh-CN")
L1_CODE = "en"   # The language you understand
L2_CODE = "es"   # The language you're learning--None is "Auto"; 
ENABLE_INITIALIZATION_DOTFILES = False # Basic .env % .tmp check
###############################

# main() decides what runs and when.
def main():

    if ENABLE_INITIALIZATION_DOTFILES:
        initialize_dotfiles()

    l2_text = extractors.clipboard_extract()

    timestamp = generate_timestamp()

    if L2_CODE is None:
        l1_text, identified_l2_code  = translators.lara_translate(raws = l2_text, lang_in = None, lang_out = L1_CODE)
    else:
        l1_text, _ = translators.lara_translate(raws = l2_text, lang_in = L2_CODE, lang_out = L1_CODE)

    if L2_CODE is None:
        print(f"{identified_l2_code}: {l2_text}")
    else:
        print(f"{L2_CODE}: {l2_text}")    

    if L2_CODE is None:
        l2_audio = voiceovers.fish_voiceover(raws=l2_text, lang_in=identified_l2_code)
    else:
        l2_audio = voiceovers.fish_voiceover(raws=l2_text, lang_in=L2_CODE)

    l2_audio_filename = "./.tmp/" + timestamp + ".mp3"
    with open(l2_audio_filename, "wb") as file:
        file.write(l2_audio)
    print(f"{L1_CODE}: {l1_text}")   
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
