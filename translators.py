#SPDX-FileCopyrightText: 2026 Josué Enrique Barredo Alamilla
#SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0

"""Machine translation services. One is local. Lara Translate: API keys from .env: LARA_ACCESS_KEY_ID and LARA_ACCESS_KEY_SECRET."""

import os
import lara_sdk, transformers

# local model tasting
local_model_name = "" #"Helsinki-NLP/opus-mt_tiny_rus-eng" #"Helsinki-NLP/opus-mt-ru-en"
tokenizer = transformers.AutoTokenizer.from_pretrained(local_model_name)
model = transformers.AutoModelForSeq2SeqLM.from_pretrained(local_model_name)

def translate_opus_mt_ru_to_en(raws="Привет, мир!"):
    tok = tokenizer(raws, return_tensors="pt").input_ids
    output = model.generate(tok)[0]
    return tokenizer.decode(output, skip_special_tokens=True)


def lara_translate(raws="!Hola, mundo!", lang_in = "es-MX", lang_out = "en"):
    """
    Translate raws string from lang_in to lang_out via Lara Translate.

    lang_in=None means auto-detect language.
    
    Returns a tuple: (translated text, detected source language code).
    Exits the process on missing keys or API errors.
    TODO proper error handling.
    """
    lara_id_key = os.environ.get("LARA_ACCESS_KEY_ID")
    lara_secret_key = os.environ.get("LARA_ACCESS_KEY_SECRET")
    if lara_id_key in ("", None) or lara_secret_key in ("", None):  # check for a remotely proper api key
        print("ERROR: At least one of the LaraTranslate API keys is missing")
        exit()

# We're letting their SDK do the heavy lifting
    credentials = lara_sdk.Credentials(lara_id_key, lara_secret_key)

    # Create translator instance
    lara = lara_sdk.Translator(credentials)
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
