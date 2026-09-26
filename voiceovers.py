#SPDX-FileCopyrightText: 2026 Josué Enrique Barredo Alamilla
#SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0
import os, random, httpx

#  i learnt i shouldn't have attempted to judge tts in languages i don't know
FISHAUDIO_VOICES = {
    "ru-RU": [  # ALL the Russian voices
        {"_id": "b871e425b6c0442baa5cf73f6c336bbe", "title": "Артём Artyom - Male Russian",},
        {"_id": "bf75c2e80b0e441485eeec20330a75fa", "title": "Полина Polina - Female Russian",},
        {"_id": "2911dfe1c9d54419b24ed8c4a1489355", "title": "Dmitri — Male young professional (RU)",},
        {"_id": "7adab54c80d34cba8c11463ab1502c9a", "title": "Maria — Female young professional (RU)",},
              ],
    "zh-CN": [  # ALL the Chinese voices whose samples were in simplified
        {"_id": "5d29a99739c14d4ca3e4fe42193105b2", "title": "梓轩 Zixuan",},
        {"_id": "74c6aba5cbf94a15bbdc547ffce5cb38", "title": "语彤 Yutong",},
        {"_id": "d675c275d1d44e57b4ef3840c5a23209", "title": "Haoran",},
        {"_id": "e98fa6cdad6946bf8d9bb8f9cb8c2532", "title": "Bingbing",},
        {"_id": "49066cb45f0a427484ade915a4474534", "title": "Ya-Ting",},
        {"_id": "e7af89da8abc4fbdacd9a10ab9881933", "title": "Chia-Hao",},
              ],
    "zh-TW": [  # ALL the Chinese voices whose samples were in traditional, excluding Cantonese
        {"_id": "91ec588cf8ef443a9c0d5b21d0c1fa36", "title": "詩涵 Shihan（台灣）",},
        {"_id": "1e85fd1e0d3e4cc2b79fbca800e7e3fe", "title": "承翰 Chenghan（台灣）",},
              ],
    "en-US": [  # Mix of most popular and least popular: should teach me how often _id s change, if ever
        {"_id": "933563129e564b19a115bedd57b7406a", "title": "Sarah",},  # first 6 that came up through 'score' sorting
        {"_id": "bf322df2096a46f18c579d0baa36f41d", "title": "Adrian",},
        {"_id": "536d3a5e000945adb7038665781a4aca", "title": "Ethan",},
        {"_id": "b347db033a6549378b48d00acb0d06cd", "title": "Selene",},
        {"_id": "9a9cf47702da476aa4629e2506d4a857", "title": "Hannah",},
        {"_id": "79d0bd3e4e5444b18f7b6d89b5927bf1", "title": "Jordan",},
        {"_id": "7882b0ed0f2a4a30bb89170985d19edc", "title": "Juno — Female conversational voice (EN)",},  # 9 assorted that caught my ear
        {"_id": "8451cb6e7e204684973f172cc616ec20", "title": "Jonah — Male companion (EN)",},
        {"_id": "f663fef9788d4ac0a6bfe36f1b3c871f", "title": "Cody — Upbeat young male (EN)",},
        {"_id": "89fe13ec21f54e40920c9a9c089d5ff3", "title": "Milo — Male companion (EN)",},
        {"_id": "1dc966a13a564043ae15591f997a3144", "title": "Sarah — Female conversational voice (EN)",},
        {"_id": "1f97ab64476c4e468a0888ae22954dab", "title": "Felix — Male companion (EN)",},
        {"_id": "94bf3b7fe581422e89d6db3653a61a38", "title": "Linda — Female companion (EN)",},
        {"_id": "84a54330a178478a88e8c9589de585a0", "title": "Wren — Female conversational voice (EN)",},
        {"_id": "18b7e3bed34d46b088b8fbd10926feb2", "title": "Michael — Male conversational voice (EN)",},  # missclassified, sounds female
              ],
    "en-GB": [  # All the Bri'ish voices
        {"_id": "0efe38923c0b445ab09382e851ae1e30", "title": "Sophia — Professional British female (EN)",},
        {"_id": "8abfa9ebd4c24a3399b68c3cdac8c7b5", "title": "Freya - Female British English",},
        {"_id": "fbc1029c018041d4b17f2c1e57222dff", "title": "Richard — Male British storyteller (EN)",},
        {"_id": "f83f2e43d24b4bccb3bd3a63a950aa93", "title": "Rupert — Composed British male (EN)",},
        {"_id": "8d8aec63a56c460cb7def795bdf754fa", "title": "Oliver - Male British English",},  # in preview it sounded a bit robotic, keep an eye
              ],
    "es-MX": [  # ALL the Mexican Spanish voices
        {"_id": "ec0718028a2445fb9be8e8bfb56a0150", "title": "Rodrigo - Male Mexican Spanish",},
        {"_id": "fbb3f56280b140c98aa41a9c1da59be6", "title": "Ximena — Female Mexican Spanish (ES)",},
        {"_id": "65793e1ac2e545bb9c56e7ca777d806a", "title": "Fernanda - Female Mexican Spanish",},
        {"_id": "61afe46cdbd64edc8361744c9f560d0c", "title": "Emiliano — Male Mexican Spanish (ES)",},
              ],
    "ja-JP": [  # i don't even know
        {"_id": "297a6fd278df47c3b9da9bfdf55ac89a", "title": "さとる(ナレーション)",},  # first 4 that came up through 'score' sorting
        {"_id": "b2d9d8db057042688a5e318b8f405bc2", "title": "きょうこ (カスタマーサポート)",},
        {"_id": "d738c70d206149e69f8e3b6fc8af9d96", "title": "じん(ラジオパーソナリティ)",},
        {"_id": "5da7f24e9e274f91b2b677669c818ce9", "title": "しおり (ナレーション)",},
        {"_id": "88b4365cf39d46e980f07cce0dab0478", "title": "結衣 Yui - Female Japanese",},  # last 2 that came up through 'score' sorting
        {"_id": "8fb06bac5bff4f51936abd2a36df1535", "title": "陽翔 Haruto - Male Japanese",},
        {"_id": "c496c7d0e93640a59a0befd78b47f39e", "title": "男の子",},  # 2 voices literally tagged 'anime' huehue
        {"_id": "bf5634e34ee5489991fe687ad0d202c5", "title": "女の子",},
              ],
    "fr-FR": [  # ALL the Gallic French voices
        {"_id": "10a3a20742114a4ea6dd441e7591850f", "title": "Manon",},
        {"_id": "f69bca092b674168a8d02d61ca20943c", "title": "Lucas",},
        {"_id": "94702e20bb3e44d39c64ba74bb480dfc", "title": "Thérèse — Female professional (FR)",},
        {"_id": "9af982ac4fbc4877af9d33b06e694fb9", "title": "Julien — Male young professional (FR)",},
        {"_id": "6bc2c46f2f5d461b9a16d9b569d665ac", "title": "Étienne — Male young professional (FR)",},
        {"_id": "3b8f4121a0d04a85bd3627ed73864f1a", "title": "Camille — Female professional (FR)",},
              ],
    "en-IN": [  # Multilingual placeholder
        {"_id": "659f2173c5e346c198ea856f5f22eb15", "title": "Aarav — Male Indian multilingual (EN)",},
              ],
                     }

# think about what possibly could you also need for a voiceover
# ELEVENLABS_VOICES = { 
#     "zh-cn": [
#         {"_id":"", "title":""}
#               ],
#     "ru-ru": [
#         {"_id":"", "title":""}
#               ],
#                      }

def fish_voiceover(raws="!Hola, mundo!", lang_in="es"):

    fishaudio_api_key = os.environ.get("FISH_API_KEY")

    if lang_in == "ru":
        fishaudio_voice = random.choice(FISHAUDIO_VOICES["ru-RU"])
    elif lang_in=="zh-TW":
        fishaudio_voice = random.choice(FISHAUDIO_VOICES["zh-TW"])
    elif lang_in=="zh":
        fishaudio_voice = random.choice(FISHAUDIO_VOICES["zh-CN"])
    elif lang_in=="ja":
        fishaudio_voice = random.choice(FISHAUDIO_VOICES["ja-JP"])
    elif lang_in=="en-GB":
        fishaudio_voice = random.choice(FISHAUDIO_VOICES["en-GB"])
    elif lang_in=="en":
        fishaudio_voice = random.choice(FISHAUDIO_VOICES["en-US"])
    elif lang_in=="es":
        fishaudio_voice = random.choice(FISHAUDIO_VOICES["es-MX"])
    elif lang_in=="fr":
        fishaudio_voice = random.choice(FISHAUDIO_VOICES["fr-FR"])
    else: 
        fishaudio_voice = FISHAUDIO_VOICES["en-IN"][0]  # Things went bad if you hear Aarav

    if fishaudio_api_key in ("", None) or fishaudio_voice in ("", None):  # check for a remotely proper api key
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
        "reference_id": fishaudio_voice["_id"],
        "format": "mp3",}

    with httpx.Client() as client:
        response = client.post(
            "https://api.fish.audio/v1/tts",
            headers=headers,
            json=body,)

    response.raise_for_status()

    voiceover = response.content

    return voiceover
