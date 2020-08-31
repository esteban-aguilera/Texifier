import os


# --------------------------------------------------------------------------------
# functions
# --------------------------------------------------------------------------------
def mkdir(dir):
    """Create a directory.  If it already exists do nothing

    Parameters
    ----------
    dir: str
        Name of the directory
    """
    if(os.path.exists(dir) is False and dir not in ['']):
        os.mkdir(dir)


def find_closing_parentheses(text, p):
    """Given a text that starts with a particular parenthesis, it finds the
    closing version of the parenthesis.

    Parameters
    ----------
    text: str
        Text that begins with a certain type of parenthesis.

    p: str
        Pair of parenthesis.  It can be '()', '{}' or '[]'

    Returns
    -------
    idx: int
        Index of the closing parenthesis.  If the parenthesis does not close, it 
        returns -1.
    """
    ii, kk = (text[0] == p[0]) - 1, text.find(p[1])   # indices

    while(kk != -1):
        ii = text.find(p[0], ii+1)  # find next opening parentheses
        if(ii != -1):   # if there is a next opening parentheses
            if(ii < kk):  # if the opening parentheses is before the closing one.
                kk = text.find(p[1], kk+1)  # find next closing parentheses
            else:
                return kk
        else:
            return kk  # there is no other opening parentheses

    return -1


def find_opening_parentheses(text, p):
    """Given a text that ends with a particular parenthesis, it finds the opening
    version of the parenthesis.

    Parameters
    ----------
    text: str
        Text that begins with a certain type of parenthesis.

    p: str
        Pair of parenthesis.  It can be '()', '{}' or '[]'

    Returns
    -------
    idx: int
        Index of the opening parenthesis.  If the parenthesis does not close, it 
        returns -1.
    """
    ii, kk = len(text) - (text[-1] == p[1]), text.rfind(p[0])   # indices

    while(kk != -1):
        ii = text.rfind(p[1], 0, ii)  # find next closing parentheses
        if(ii != -1):  # if there is a next closing parentheses
            if(kk < ii):  # if there is a next opening parentheses
                kk = text.rfind(p[0], 0, kk)  # find next opening parentheses
            else:
                return kk
        else:
            return kk  # there is no other parentheses

    return -1


def find_all(s, ch):
    """It receives an string and a character.  It returns every index where
    the character appears in the string.

    Parameters
    ----------
    s: str
        String where the character will be looked for.

    ch: str
        Character of interest.

    Returns
    -------
    indices: list
        List of indices where ch appear in s.
    """
    return [i for i, letter in enumerate(s) if letter == ch]


def check_parentheses(text):
    """Check if every parenthesis in a text is in pairs.

    Parameters
    ----------
    text: str
        Text with parenthesis

    Raises
    ------
    Exception: If a parenthesis does not open/close
    """
    for p in ['()', '[]', '{}']:
        for i in find_all(text, p[0]):
            k = find_closing_parentheses(text[i:], p)
            if(k == -1):
                nline = text[:i].count('\n') + 1
                start, end = text[:i].rfind('\n') , text.find('\n', i)
                print()
                raise Exception(f"""Parentheses {p[0]} in line {nline} does not close:
                    {text[start:i]}\033[4m{p[0]}\033[0m{text[i+1:end]}
                """)

        for i in find_all(text, p[1]):
            k = find_opening_parentheses(text[:i], p)
            if(k == -1):
                nline = text[:i].count('\n') + 1
                start, end = text[:i].rfind('\n'), text.find('\n', i)
                print()
                raise Exception(f"""Parentheses {p[1]} in line {nline} does not open:
                    {text[start:i]}\033[4m{p[1]}\033[0m{text[i+1:end]}
                """)
