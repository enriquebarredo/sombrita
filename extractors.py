#SPDX-FileCopyrightText: 2026 Josué Enrique Barredo Alamilla
#SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0

"""Text extraction. Today it's clipboard only. Tomorrow, it will be OCR from a screen overlay."""

import time
import pyperclip

def clipboard_extract():
    """
    Blocks until clipboard holds something new, then returns it.

    Sets a sentinel (U+E000, private use area char no real text uses),
    into the clipboard and polls until user copies something real.
    """

    sentinel_char = "\uE000"
    pyperclip.copy(sentinel_char)  # clr system clipboard
    raws = sentinel_char
    print(f"{raws}: Listening on clipboard")
    while raws == sentinel_char:   # test if content still has the sentinel value
        time.sleep(0.1)
        raws = pyperclip.paste()

    return raws
