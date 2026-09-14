#SPDX-FileCopyrightText: 2026 Josué Enrique Barredo Alamilla
#SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0

# main.py decides what runs and when.
# After settings are implemented, main will read from there and call whichever and however they apply

from dotenv import load_dotenv
load_dotenv()
import translator
import voiceover
import extractor

########## config #############
# Full explanation: https://developers.laratranslate.com/docs/supported-languages
# Short explanation: Strings  2-letter codes for langs (ISO639) and regions (optional, separated by a dash) ("es-MX", "fr-CA", "zh")
user_l1 = "en"   # The language you understand well enough
user_l2 = None   # The language you're learning--None auto-selects; 
###############################
# Это - простой тестовый фрагмент текста для проверки синтеза речи и перевода--звучу ли я приемлемо?
def main():
    l2_text = extractor.clipboard_extract()

    if user_l2 == None:
        l1_text, found_l2   = translator.lara_translate(out_lang = user_l1, in_lang = None, in_text = l2_text)
    else:
        l1_text, _          = translator.lara_translate(out_lang = user_l1, in_lang = user_l2, in_text = l2_text)

    print(f"{user_l1}: {l1_text}")

    if user_l2 == None:
        print(f"{found_l2}: {l2_text}")
    else:
        print(f"{user_l2}: {l2_text}")    

    voiceover.fish_voiceover(l2_text)

if __name__ == "__main__":
    main()
