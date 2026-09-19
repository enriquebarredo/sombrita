<!-- SPDX-FileCopyrightText: 2026 Josué Enrique Barredo Alamilla -->
<!-- SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0 -->

[![License: PolyForm NonCommercial](https://img.shields.io/badge/License-PolyForm%20NonCommercial-b5261e?style=flat-square)](https://polyformproject.org/licenses/noncommercial/1.0.0)

# Sombrita
## Small shadowing tool
This is a personal language-learning script for shadowing text that doesn't have voiceovers. The inspirations are Alexander Argüelles' language-learning technique, the Assimil textbooks, Artikash's Textractor, and LanguageReactor. Basically, I wanted bargain-bin Assimil-on-demand material for my reading.

## Basic Goal
Use OCR (optical character recognition) to grab any L2 (target/second language) text fragment, get TTS (text-to-speech) voiceover, MT (machine translate) the fragment into L1 (dominant/native language), and display both L1 and L2 fragments as a scrollable bilingual parallel text alongside voiceover playback. The initial work is partitioned in [this diagram](https://drive.google.com/file/d/13t0PHqii64TSU_ZIgV0khLEWL3ViDuJ7/view?usp=sharing)

## Desiderata
Roughly ordered according to priority. A checkmark means it's working:
- [x] Grab L2 text from the clipboard.
- [x] Get TTS from cheapest high-quality online provider (Fish Audio)
- [x] Get L1 text from free MT (machine translation) online provider (Lara Translate)
- [ ] Store and load-up previously generated L1, L2 and voiceovers.
- [ ] Display L1, L2 and playback voiceovers in a browsable bilingual backlog.
- [ ] Grab L2 text from screenshots taken from an adjustable overlay frame on the screen.
- [ ] User customization for fonts, text size, spacing, voices.
- [ ] Recording to listen to oneself and get feedback on one's own pronunciation, a la Anki.
- [ ] Support typewriter-effect (text reveal character-by-character) in games/VNs (image processing).
- [ ] Look if LLM could offer different translation styles (from literal to natural...).
- [ ] LLM-generated romanization and linguistic gloss, though this might be helpful only to absolute beginners...
- [ ] Add local replacements for online services (MT, TTS, OCR) with settings to support a range of hardware specs (from potato PC/purely online, to beefy PC/purely local...)

## TODO
Braindump:
- Implement basic local OCR (make it expect a clipped screenshot with constant filename)
- Implement basic API calls for OCR (same clipped screenshot method)
- Implement basic elevenlabs API calls as alternative TTS.
- Get and hardcode all default official/copyright-free voice IDs from fish.audio as fallback (for en, es, fr, jp, zh, ru, at least)
    - Write the logic in `voiceovers.fish_voiceover()` to select a voice id according to a passed variable (`user_l2`/`identified_l2`)
- Look into PyQt/Side6, break up the GUI into workable conceptual blocks for drafting/planning a diagram.
- Add logic to enable turning off/on features in the pipeline (e.g. TTS only, MT only, OCR-only etc.)
- Look deeper into APIs I already work with.
- Implement proper error handling for API functions.
- Decide on a persistence layer for outputs: csv, json, sqlite3.
    - Output L1/L2 texts and .mp3 into persistent storage.
    - Write logic to read from persistence layer to display it.
- Generate the example `.env` variable names for Sombrita on first run (define dictionary, then check for every variable name and write only if missing).
- Rewrite `main()` and `extractors.py` (currently single-shot launch-and-exit run), to a looping run with exit condition.
- Write to multiple folders according to L2 language (maybe L2-L1 pairs?)
- Generate `requirements.txt` and test portability (pipreqs . --force --ignore .venv,.temp)
- Evaluate adoption of other TTS and MT API providers, test lang pairs and figure out if pricing is acceptable, which WILL TAKE TIME (Yandex is great for Russian TTS, and its Russian-Spanish MT is helpfully literal, like a halfway point between a gloss and a normal translation, but it's probably bad for everything else; Elevenlabs mispronounces even common hanzi in common Chinese words, but it's excellent for everything else; never heard of Microslop Translator but I wanna try it; etc...).

## The name
Because the script relies on MT, I wanted something that references the non-sequiturs you get from recursive MT: 'A small shadowing tool' -> 'una pequeña sombra' -> 'umbrella' -> 'sombrita'. A silly name for a silly tool.

## Licensing
Unless otherwise noted, everything in this repository is licensed under the PolyForm Noncommercial License 1.0.0.
For details, refer to the full text of the [license](./LICENSE), which is also available [online](https://polyformproject.org/licenses/noncommercial/1.0.0).
