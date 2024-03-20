from colorama import just_fix_windows_console
just_fix_windows_console()

###################################################################################################################
###################################################################################################################

def ColoredPrint(formatStr : str):
    """
    Colored output to console. Uses ANSI standard.
    
    Escape sequences, that changes text color:
        #d - dark
        #r - red
        #g - green
        #y - yellow
        #b - blue
        #m - magenta
        #c - cyan
        #w - white

    Escape sequences, that changes background color:
        #bx - (background + x-color), where x - is text color letter (see previous paragraph).

    Escape sequences, that changes font style:
        #rs - reset text style to normal console style
        #bl - bold
        #p  - pale
        #i  - italic.
        #u  - underlined
        #bk - blinking
        #cr - crossed out

    No operations escape sequence. It do not nothing. You can use it for pretty format string aligning:
        #_ - This sequence is deleted in resulting string. You can use any number of '_' after '#'.

    After escape sequence, it is possible to place any number of '_' for pretty aligning. Next sequences are equivalent:
        #d___#r
        #d#r____
        #d__#r___
        #d_#r_
        #d#r

    Sharp symbol: ##
    """

    outStr = ""
    escapes = [
        ("rs", "0"), 
        ("bl", "1"), 
        ("p",  "2"), 
        ("i",  "3"), 
        ("u",  "4"), 
        ("bk", "5"), 
        ("cr", "9"),
        
        ("bd", "40"),
        ("br", "41"), 
        ("bg", "42"), 
        ("by", "43"), 
        ("bb", "44"),
        ("bm", "45"), 
        ("bc", "46"), 
        ("bw", "47"),

        ("d",  "30"), 
        ("r",  "31"), 
        ("g",  "32"), 
        ("y",  "33"), 
        ("b",  "34"), 
        ("m",  "35"), 
        ("c",  "36"), 
        ("w",  "37")
    ]
    escStart = "\033["
    escSep   = ";"
    escEnd   = "m"
    
    formatStrLen = len(formatStr)
    isDoubleEsq = False
    st = 0

    def AppendChar():
        nonlocal outStr
        nonlocal formatStr
        nonlocal st
        nonlocal isDoubleEsq, st

        if (isDoubleEsq == True):
            outStr += escEnd
            isDoubleEsq = False

        outStr += formatStr[st]
        st += 1

    while st < formatStrLen:
        if (formatStr[st] != "#"):
            AppendChar()
            continue

        if (st + 1 < formatStrLen and formatStr[st + 1] == "#"):
            AppendChar()
            st += 1
            continue

        if (st + 1 < formatStrLen and formatStr[st + 1] == "_"):
            st += 2
            while st < formatStrLen and formatStr[st] == "_":
                st += 1
            continue

        foundEscape = False
        for (escSeq, escCode) in escapes:
            if (str.startswith(formatStr, escSeq, st + 1, formatStrLen) == False):
                continue
            
            if (isDoubleEsq == False):
                outStr += escStart + escCode
                isDoubleEsq = True
            else:
                outStr += escSep + escCode
            st += len(escSeq) + 1
            while st < formatStrLen and formatStr[st] == "_":
                st += 1
            foundEscape = True
            break

        if (foundEscape == False):
            AppendChar()
            
    if (isDoubleEsq == True):
        outStr += escEnd
        
    print(outStr)
# !ColoredPrint()

###################################################################################################################
###################################################################################################################