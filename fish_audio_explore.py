#fish_audio_explore.py
import dotenv, os, requests, json
dotenv.load_dotenv()

################### edit here
domain = "https://api.fish.audio/model?"
paging = "page_size=20&page_number=1"
sort = "sort_by=score" # "sort_by=task_count" "sort_by=created_at"
author = "author_id=d8b0991f96b44e489422ca2ddf0bd31d"  # official fish audio. it's the one with the copyright? 'no-risk!' logo.
lang = "language=ru"  #fish.audio/model? does not have a dictionary entry for regional variants. no "zh-tw", no "yue-hk" just "zh". some have it under tags. some.
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

interesting_keys = ["_id", "title", "description", "tags", "samples"]
list_of_voices = []
for u in range(response_dict["total"]):
    voice = {"_id": "", "title": "", "description": "", "tags": "", "samples": ""}  # every voice is a dictionary
    voice["_id"] = response_dict["items"][u]["_id"]
    voice["title"] = response_dict["items"][u]["title"]
    voice["description"] = response_dict["items"][u]["description"]
    voice["tags"] = response_dict["items"][u]["tags"]
    voice["samples"] = response_dict["items"][u]["samples"]
    list_of_voices += [voice]

interesting_keys = ["_id", "title", "description", "tags", "samples"]
list_of_voices = []
for u in range(response_dict["total"]):
    voice = {} # every voice is a dictionary
    for v in range(len(interesting_keys)):
        voice[interesting_keys[v]] = response_dict["items"][u][interesting_keys[v]]
    list_of_voices += [voice]

with open(filename, "w") as file:
    json.dump(list_of_voices, file, indent = 2, ensure_ascii= False)

# goal, let's play and see what data could even be relevant
