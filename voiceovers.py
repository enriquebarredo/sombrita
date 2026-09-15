#SPDX-FileCopyrightText: 2026 Josué Enrique Barredo Alamilla
#SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0

import os, httpx

def fish_voiceover(raws="!Hola, mundo!"):

    fishaudio_api_key = os.environ.get("FISHAUDIO_API_KEY")
    fishaudio_voice_id = os.environ.get("FISHAUDIO_VOICE_ID")
    if fishaudio_api_key in ("", None) or fishaudio_voice_id in ("", None):  # check for a remotely proper api key
        print("ERROR: At least one of the fish.audio API keys is missing")
        exit()

# For the free voiceover, fish.audio requires doing it by hand.
    # JSON for TTS
    headers = {
        "Authorization": f"Bearer {fishaudio_api_key}",
        "Content-Type": "application/json",
        "model": "s2.1-pro-free",}
    body = {
        "text": raws, # main input variable goes here
        "reference_id": fishaudio_voice_id,
        "format": "mp3",}

    with httpx.Client() as client:
        response = client.post(
            "https://api.fish.audio/v1/tts",
            headers=headers,
            json=body,)

    response.raise_for_status()

    dubs = response.content

    return dubs
