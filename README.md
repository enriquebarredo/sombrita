<!-- SPDX-FileCopyrightText: 2026 Josué Enrique Barredo Alamilla -->
<!-- SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0 -->

[![License: PolyForm NonCommercial](https://img.shields.io/badge/License-PolyForm%20NonCommercial-b5261e?style=flat-square)](https://polyformproject.org/licenses/noncommercial/1.0.0)

# Sombrita
## Small shadowing tool
This is a personal language-learning script for shadowing text that doesn't have voiceovers. The inspirations are Alexander Argüelles' language-learning technique, the Assimil textbooks, Artikash's Textractor, and LanguageReactor. Basically, I wanted bargain-bin Assimil-on-demand material for my reading.

## Basic Goal
Grab any L2 (target language) text, MT it into L1 (dominant language), display both L1 and L2 as dual subtitles and generate a TTS voiceover. The initial work is partitioned in [this diagram](https://drive.google.com/file/d/13t0PHqii64TSU_ZIgV0khLEWL3ViDuJ7/view?usp=sharing)

## Desiderata
Roughly ordered according to priority:
- Grab L2 text from the clipboard.
- Get TTS from fish.audio (cheapest option)
- Get MT from LaraTranslate (free-tier option)
- Display outputs in a browsable bilingual backlog, where each line replays its corresponding TTS voiceover.
- Grab L2 text from OCR, via an adjustable overlay frame on the screen.
- Evaluate adoption of other TTS and MT API providers, test lang pairs and figure out if pricing is acceptable, which WILL TAKE TIME (Yandex is great for Russian TTS, and its Russian-Spanish MT is helpfully literal, like a halfway point between a gloss and a normal translation, but it's probably bad for everything else; Elevenlabs mispronounces even common hanzi in common Chinese words, but it's excellent for everything else; never heard of Microslop Translator but I wanna try it; etc...).
- User customization for fonts, text size, spacing, voices.
- Recording to listen to oneself and get feedback on one's own pronunciation, a la Anki.
- Image processing to support the typewriter-effect text popular in games/VNs.
- Looking into LLM setup to enable different translation styles.
- LLM-enabled romanization and linguistic gloss might be helpful only to absolute beginners...
- Add API replacements to support a range of hardware specs (from potato PC, to beefy PC...)

## The name
Because the script relies on MT, I wanted something that references the non-sequiturs you get from recursive MT: 'A small shadowing tool' -> 'una pequeña sombra' -> 'umbrella' -> 'sombrita'. A silly name for a silly tool.

## Licensing
Unless otherwise noted, everything in this repository is licensed under the PolyForm Noncommercial License 1.0.0.
For details, refer to the full text of the [license](./LICENSE), which is also available [online](https://polyformproject.org/licenses/noncommercial/1.0.0).
