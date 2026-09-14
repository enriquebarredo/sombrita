#SPDX-FileCopyrightText: 2026 Josué Enrique Barredo Alamilla
#SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0

import pyperclip, time

def clipboard_extract():
    pyperclip.copy("\uE000")    # clr actual clipboard
    clpbrd_cntnt = "\uE000"     # clr local working clipboard value
    print(f"{clpbrd_cntnt}: Listening on clipboard")         # test sentinel value
    while clpbrd_cntnt == "\uE000":
        time.sleep(0.1)
        clpbrd_cntnt = pyperclip.paste()

    return clpbrd_cntnt
