#SPDX-FileCopyrightText: 2026 Josué Enrique Barredo Alamilla
#SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0

# main.py decides what runs and when.
# After settings are implemented, main will read from there and call whichever and however they apply

from dotenv import load_dotenv
load_dotenv()
import translators
import voiceovers
import extractors

########## config #############
# Full explanation: https://developers.laratranslate.com/docs/supported-languages
# Short explanation: Strings  2-letter codes for langs (ISO639) and regions (optional, separated by a dash) ("es-MX", "fr-CA", "zh")
user_l1 = "en"   # The language you understand well enough
user_l2 = None   # The language you're learning--None auto-selects; 
###############################
# Это - простой тестовый фрагмент текста для проверки синтеза речи и перевода--звучу ли я приемлемо?
def main():
    l2_text = extractors.clipboard_extract()

    if user_l2 == None:
        l1_text, identified_l2   = translators.lara_translate(raws = l2_text, lang_in = None, lang_out = user_l1)
    else:
        l1_text, _          = translators.lara_translate(raws = l2_text, lang_in = user_l2, lang_out = user_l1)

    print(f"{user_l1}: {l1_text}")

    if user_l2 == None:
        print(f"{identified_l2}: {l2_text}")
    else:
        print(f"{user_l2}: {l2_text}")    

    l2_audio = voiceovers.fish_voiceover(raws=l2_text)

    # need to save a timestamp as the filename
    with open("./.tmp/voiceover.mp3", "wb") as file:
        file.write(l2_audio)
    print("✓ Audio saved to ./.tmp/voiceover.mp3")

if __name__ == "__main__":
    main()
