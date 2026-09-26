#fish_audio_explore.py
import dotenv, os, requests, json
dotenv.load_dotenv()

# GOAL: notice useful things from data. NOTICED:
# audio samples are revealing, titles are human-readable, but there's very few meaningful things from title, description or most tags.
# fallback voices: pure task count should discourage Fish Audio from expunging their voice model, which gives 
# "score" is some internal popularity metric. "task_count" is a usage metric. if there are too many voices, i should use both.
################### edit here
domain = "https://api.fish.audio/model?"
paging = "page_size=100&page_number=1"   #  will only take the top half of those sorted
sort = "sort_by=score"  # "sort_by=task_count" "sort_by=created_at"
author = "author_id=d8b0991f96b44e489422ca2ddf0bd31d"  # official fish audio. it's the one with the copyright? 'no-risk!' logo.
# they don't have a dictionary entry for regional variants: there are "zh-tw" and "yue-hk" under some tags, but just "zh" under "language", and sometimes, the only reference to a variety is found in the title
lang = "language=tr"
lang2 = "language=en"  #but you can look up voices with expressed support for multiple languages

url_options = [paging, sort, author, lang]
url = domain + "&".join(url_options)  # requests.get has ways to pass parameters, but managing strings feels more grounded.

fishaudio_api_key = os.environ.get("FISH_API_KEY")

headers = {"Authorization": f"Bearer {fishaudio_api_key}"}
response = requests.get(url, headers=headers)
response.raise_for_status()

response_dict = response.json()

filename = f"./.tmp/full_response_{lang[-2:]}.json"
# with open(filename, "w") as file:
#     file.write(response.text)
with open(filename, "w") as file:
    json.dump(response_dict, file, indent = 2, ensure_ascii= False)  #looking up data for foreign languages, last part is necessary
#  fish.audio/model? does not return a dictionary entry for regional variants

filename = f"./.tmp/summarized_response_{lang[-2:]}.json"  # the whole response has too much junk

# crazy idea, adding a simple 'popularity' score: just a ratio of likes per tasks tells me how much crowds like a voice.
interesting_keys = ["_id", "title", "description", "tags", "samples", "like_count", "mark_count", "shared_count", "task_count"]
list_of_voices = []
for u in range(response_dict["total"]):
    voice = {} # every voice is a dictionary
    for v in range(len(interesting_keys)):
        voice[interesting_keys[v]] = response_dict["items"][u][interesting_keys[v]]
    # These metrics below only help if the task_counts are large enough and there are more than 10 voices. They're just noise, otherwise.
    voice["likes per 1000"] = voice["like_count"] / voice["task_count"] * 1000 if voice["task_count"] != 0 else 0
    voice["bookmarks per 1000"] = voice["mark_count"] / voice["task_count"] * 1000 if voice["task_count"] != 0 else 0
    list_of_voices += [voice]

with open(filename, "w") as file:
    json.dump(list_of_voices, file, indent = 2, ensure_ascii= False)
