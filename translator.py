#SPDX-FileCopyrightText: 2026 Josué Enrique Barredo Alamilla
#SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0

import os
from lara_sdk import Credentials, Translator  #  for the lararium
def lara_translate(l1 = "es", l2 = "en", l2_text="Hello, world!"):

    lara_api_key = os.environ.get("LARA_ACCESS_KEY_ID")
    lara_access_key = os.environ.get("LARA_ACCESS_KEY_SECRET")
    if lara_api_key in ("", None) or lara_access_key in ("", None):  # check for a remotely proper api key
        print("ERROR: At least one of the LaraTranslate API keys is missing")
        exit()
# We're letting SDK do the heavy lifting
    credentials = Credentials(lara_api_key, lara_access_key)

    # Create translator instance
    lara = Translator(credentials)
    # Simple text translation
    try:
        l1_text = lara.translate(l2_text, target=l1, source=l2)
        print(f"L1: {l1_text.translation}")
        # Output: "Translation: !Hola, mundo!"?
    except Exception as error:
        print(f"Translation error: {error}")

    return l1_text
