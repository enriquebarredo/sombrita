#SPDX-FileCopyrightText: 2026 Josué Enrique Barredo Alamilla
#SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0

import pyperclip, time

def clipboard_extract():
    pyperclip.copy("\uE000")            # clr system clipboard
    raws = "\uE000"     # 
    print(f"{raws}: Listening on clipboard")
    while raws == "\uE000":          # test if content still has the sentinel value
        time.sleep(0.1)
        raws = pyperclip.paste()

    return raws
