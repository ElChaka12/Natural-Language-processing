# syllable.py
# -----------
# This module contains one function: extract_syllable(word)
# It takes a Setswana word and breaks it into its syllable parts.
# It can also be run directly as a script to test a single word.


def extract_syllable(word):
    """
    Breaks a Setswana word into a list of syllables.

    Parameters:
        word (str): A single Setswana word (lowercase letters).

    Returns:
        list: A list of syllable strings found in the word.

    Examples:
        extract_syllable("mosadi")  -> ['mo', 'sa', 'di']
        extract_syllable("tlhalo")  -> ['tlha', 'lo']
        extract_syllable("ebela")   -> ['e', 'be', 'la']
    """

    # p  = syllable counter (how many syllables found so far)
    p = 0

    # lastchar = the previous character we looked at (starts empty)
    lastchar = ""

    # s  = the syllable currently being built up, character by character
    s = ""

    # sp = the previous value of s before the last character was added
    #      (used to look back one step when handling special cases like "ng")
    sp = ""

    # syllables = the final list we fill up and return
    syllables = []

    # The five Setswana vowels that end a syllable
    vowels = ["a", "e", "i", "o", "u"]

    # ── Main loop: go through every character in the word ──────────────────────
    for i in range(len(word)):

        # Pull out character at position i  (word[i:i+1] is safer than word[i]
        # because it returns "" instead of crashing if i is out of range)
        c = word[i:i+1]

        # ── Case 1: current character is a CONSONANT ────────────────────────
        if c not in vowels:
            sp = s          # save the syllable-so-far before we add this consonant
            s  = s + c      # add the consonant to the growing syllable

        # ── Case 2: current character is a VOWEL ───────────────────────────
        else:
            s = s + c           # add the vowel to complete the syllable
            syllables.append(s) # the syllable is now finished — save it
            p += 1              # count it
            s  = ""             # reset the buffer for the next syllable

        # ── Special case: "ng" cluster ──────────────────────────────────────
        # Setswana treats "ng" as its own syllable unit in certain positions.
        # If the previous two characters formed "ng", AND the current character
        # is NOT "w" AND is NOT a vowel, then "ng" should be its own syllable.
        if sp == "ng" and c != "w" and c not in vowels:
            syllables.append("ng")  # save "ng" as a standalone syllable
            p += 1
            s = c                   # the current consonant starts the next syllable

        # ── Special case: "n" followed by another consonant ────────────────
        # In Setswana, when "n" is followed by most consonants (not g/y/w or
        # a vowel), it acts as a standalone nasal syllable.
        if lastchar == "n":
            if c != "g" and c != "y" and c != "w" and c not in vowels:
                # "n" on its own is a syllable; start fresh with current consonant
                syllables.append(sp)    # sp holds the "n" we saw previously
                p += 1
                s = ""
                s = c               # current consonant begins the next syllable
            else:
                # Special sub-case: "ng" at the very END of the word
                # e.g. the "-ng" suffix in Setswana (present tense marker)
                if c == "g" and i == len(word) - 1:
                    syllables.append(s)  # save "ng" as the final syllable
                    p += 1
                    s = ""

        # ── Special case: "m" followed by m/p/b/h ──────────────────────────
        # Setswana has prenasalised consonants like "mm", "mp", "mb", "mh".
        # When "m" is immediately followed by one of these, the "m" before it
        # becomes its own syllable and the new consonant starts a fresh one.
        if lastchar == "m":
            if c == "m" or c == "p" or c == "b" or c == "h":
                syllables.append(sp)    # save the lone "m" syllable
                p += 1
                s = c                   # start fresh with the new consonant

        # Remember this character so the next loop iteration can look back at it
        lastchar = c

    return syllables


# ── Entry point: runs only when this file is executed directly ─────────────────
# When you type:  python syllable.py
# Python sets __name__ to "__main__", so this block runs.
# When another file imports this module, this block is SKIPPED.
if __name__ == "__main__":
    word = "atamelane"
    print("The word is: ", word)
    print("The syllables are: ", extract_syllable(word))
