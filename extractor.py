import pyperclip, time

def clipboard_extract():
    pyperclip.copy("\uE000")    # clr actual clipboard
    clpbrd_cntnt = "\uE000"     # clr local working clipboard value
    print(clpbrd_cntnt)         # test sentinel value
    while clpbrd_cntnt == "\uE000":
        time.sleep(0.1)
        clpbrd_cntnt = pyperclip.paste()
    print(f"L2: {clpbrd_cntnt}")
    return clpbrd_cntnt
