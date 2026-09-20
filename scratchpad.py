#scratchpad.py
import dotenv, os, requests
dotenv.load_dotenv()

################### edit here
domain = "https://api.fish.audio/model?page_size=10"
boilerplate = "page_number=1"
sort = "sort_by=score" # "sort_by=task_count" "sort_by=created_at"
author = "author_id=d8b0991f96b44e489422ca2ddf0bd31d"  # official fish audio author. copyright? 'no-risk'.
lang = "language=en"
lang2 = "language=es" # you can add multiple languages
#url = "https://api.fish.audio/model?page_size=10&page_number=1&sort_by=score&author_id=d8b0991f96b44e489422ca2ddf0bd31d&language=zh"
url_options = [domain, boilerplate, sort, author, lang]
url = "&".join(url_options)

fishaudio_api_key = os.environ.get("FISH_API_KEY")

headers = {"Authorization": f"Bearer {fishaudio_api_key}"}
response = requests.get(url, headers=headers)
response.raise_for_status()

filename = f"./.tmp/response_{lang[-2:]}.txt"
with open(filename, "w") as file:
    file.write(response.text)

# goal, let's play and see what data could even be relevant
