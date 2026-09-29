#SPDX-FileCopyrightText: 2026 Josué Enrique Barredo Alamilla
#SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0

"""fish_audio_explore.py lists Fish Audio voice models as a scratch script"""

import json, os
import dotenv, requests

dotenv.load_dotenv()

# Findings so far:
# audio samples tell you if you're gonna tolerate a voice
# title, description and most tags carry very little meaningful information
# title is human-readable and unique enough
# "score" order is sort of a popularity order. "task_count" is usage metric.
#   both metrics above neglect newer voices
#   but the more a voice is used, the more Fish Audio is encouraged to maintain it.
# I want fallback voices to be as stable as possible
# but if i want to notice how often, if ever, Fish Audio retires/expunges official voices,
#   I should keep a few hardcoded as well.

################### edit here
domain = "https://api.fish.audio/model?"
paging = "page_size=100&page_number=1"  # maximum of 100. but en, the most popular language, still has under 80 voices
sort = "sort_by=score"  # alternatives: "sort_by=task_count" "sort_by=created_at"
# "Fish Official"-authored voices carry a 'safe-voice-badge.svg':
# 'AI-designed voice, not cloned from any real person; no copyright risk'
author = "author_id=d8b0991f96b44e489422ca2ddf0bd31d"
# Standard 2-character ISO codes; no regional variants: "zh" for Chinese, only.
# you might find "zh-tw" and "yue-hk" in voice tags, or referenced in a voice's title
lang = "language=tr"
lang2 = "language=en"  # a voice can declare support for several languages (only Aarav in the official voices, though)
  # requests.get can pass parameters, but managing strings feels more grounded when it's this trivial
url_options = [paging, sort, author, lang]
url = domain + "&".join(url_options)

fishaudio_api_key = os.environ.get("FISH_API_KEY")

headers = {"Authorization": f"Bearer {fishaudio_api_key}"}
response = requests.get(url, headers=headers)
response.raise_for_status()

response_dict = response.json()

filename = f"./.tmp/full_response_{lang[-2:]}.json"
with open(filename, "w") as file:
    json.dump(response_dict, file, indent = 2, ensure_ascii= False)
# ensure_ascii= False keeps multilingual text readable

# The full response has too much junk; keep only the interesting fields.
filename = f"./.tmp/summarized_response_{lang[-2:]}.json"
# crazy idea, adding a simple 'popularity' score: just a ratio of likes per tasks tells me how much crowds like a voice.
# These metrics below only help if the task_counts are large enough and there are more than 10 voices. They're just noise, otherwise.
interesting_keys = ["_id", "title", "description", "tags", "samples", "like_count", "mark_count", "shared_count", "task_count"]
list_of_voices = []
for u in range(response_dict["total"]):
    voice = {}
    for v in range(len(interesting_keys)):
        voice[interesting_keys[v]] = response_dict["items"][u][interesting_keys[v]]
    voice["likes per 1000"] = voice["like_count"] / voice["task_count"] * 1000 if voice["task_count"] != 0 else 0
    voice["bookmarks per 1000"] = voice["mark_count"] / voice["task_count"] * 1000 if voice["task_count"] != 0 else 0
    list_of_voices += [voice]

with open(filename, "w") as file:
    json.dump(list_of_voices, file, indent = 2, ensure_ascii= False)
