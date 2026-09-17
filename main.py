#SPDX-FileCopyrightText: 2026 Josué Enrique Barredo Alamilla
#SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0

import datetime
from dotenv import load_dotenv
load_dotenv()
import translators
import voiceovers
import extractors

# Это - простой тестовый фрагмент текста для проверки синтеза речи и перевода--звучу ли я приемлемо?
########## config #############
# Full explanation: https://developers.laratranslate.com/docs/supported-languages
# Short explanation: Strings of 2-letter codes for langs (ISO639) and regions (optional, prefixed with a dash: "es-MX", "fr-CA", "zh-CN")
user_l1 = "en"   # The language you understand well enough
user_l2 = None   # The language you're learning--None auto-selects; 
###############################

# main() decides what runs and when.
def main():
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


if __name__ == "__main__":
    main()
