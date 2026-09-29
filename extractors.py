#SPDX-FileCopyrightText: 2026 Josué Enrique Barredo Alamilla
#SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0

"""Text extraction. Today it's clipboard only. Tomorrow, it will be OCR from a screen overlay."""

import time
import pyperclip

def clipboard_extract():
    """
    Blocks until clipboard holds something new, then returns it.

    Sets a SENTINEL (U+E000, private use area char no real text uses),
    into the clipboard and polls until user copies something real.
    """

    SENTINEL_CHAR = "\uE000"
    pyperclip.copy(SENTINEL_CHAR)  # clr system clipboard
    raws = SENTINEL_CHAR
    print(f"{raws}: Listening on clipboard")
    while raws == SENTINEL_CHAR:   # test if content still has the sentinel value
        time.sleep(0.1)
        raws = pyperclip.paste()

    return raws
