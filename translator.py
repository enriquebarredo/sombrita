#SPDX-FileCopyrightText: 2026 Josué Enrique Barredo Alamilla
#SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0

import os
from lara_sdk import Credentials, Translator  #  for the lararium
def lara_translate(out_lang = "en", in_lang = "es-MX", in_text="!Hola, mundo!"):

    lara_api_key = os.environ.get("LARA_ACCESS_KEY_ID")
    lara_access_key = os.environ.get("LARA_ACCESS_KEY_SECRET")
    if lara_api_key in ("", None) or lara_access_key in ("", None):  # check for a remotely proper api key
        print("ERROR: At least one of the LaraTranslate API keys is missing")
        exit()
# We're letting their SDK do the heavy lifting
    credentials = Credentials(lara_api_key, lara_access_key)

    # Create translator instance
    lara = Translator(credentials)
    # Simple text translation
    try:
        textresult = lara.translate(in_text, target=out_lang, source=in_lang)
        l1_text = textresult.translation
        autodetected_l2 = textresult.source_language
    except Exception as error:
        print(f"LaraTranslate translation error: {error}")
        exit()
    
#    print(lara.languages())
    return l1_text, autodetected_l2
