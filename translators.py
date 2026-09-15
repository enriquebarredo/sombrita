#SPDX-FileCopyrightText: 2026 Josué Enrique Barredo Alamilla
#SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0

import os

from lara_sdk import Credentials, Translator  #  for the lararium
def lara_translate(raws="!Hola, mundo!", lang_in = "es-MX", lang_out = "en"):

    lara_id_key = os.environ.get("LARA_ACCESS_KEY_ID")
    lara_secret_key = os.environ.get("LARA_ACCESS_KEY_SECRET")
    if lara_id_key in ("", None) or lara_secret_key in ("", None):  # check for a remotely proper api key
        print("ERROR: At least one of the LaraTranslate API keys is missing")
        exit()

# We're letting their SDK do the heavy lifting
    credentials = Credentials(lara_id_key, lara_secret_key)

    # Create translator instance
    lara = Translator(credentials)
    # Simple text translation
    try:
        textresult = lara.translate(raws, source=lang_in, target=lang_out)
        subs = textresult.translation
        identified_lang = textresult.source_language
    except Exception as error:
        print(f"LaraTranslate translation error: {error}")
        exit()
    
#    print(lara.languages())
    return subs, identified_lang
