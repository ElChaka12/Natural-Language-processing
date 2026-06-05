# syllable_test_code.py
# ---------------------
# This script reads a Setswana word-game text file, extracts syllables from
# every base word using the extract_syllable() function, and prints out all
# words whose base word has a CHOSEN number of syllables, together with their
# related word group.
#
# HOW TO RUN:
#   Make sure "Word game text file.txt" is in the same folder, then run:
#       python syllable_test_code.py
#
# FILE FORMAT (one line per word group):
#   ebela,bela,lae,ela,beela
#   tshabela,tshabe,bela
#   (ngwaela),ngwae,ela,lae        <- brackets mean the first word is excluded
#                                     from being the base word


# Import the extract_syllable function from the syllable module (syllable.py).
# This gives us access to the function without copying its code here.
from syllable import extract_syllable


# ── Step 1: Read the text file ─────────────────────────────────────────────────

# Open the file in read mode ("r").
# The 'with' keyword automatically closes the file when the block finishes,
# even if an error occurs — safer than calling f.close() manually.
with open("Word game text file.txt", "r") as f:
    # Read the entire file as one string, then split it into a list of lines.
    # Each line becomes one element in the list.
    all_sentences = f.read().split("\n")


# ── Step 2: Choose the syllable count to filter by ────────────────────────────

# Change this number to show words with a different syllable count.
# For example:
#   TARGET_SYLLABLE_COUNT = 3   -> shows 3-syllable base words
#   TARGET_SYLLABLE_COUNT = 5   -> shows 5-syllable base words (original behaviour)
#   TARGET_SYLLABLE_COUNT = 0   -> shows ALL words (no filter)
TARGET_SYLLABLE_COUNT = 0


# ── Step 3: Process each line ─────────────────────────────────────────────────

# This list will hold the formatted result strings we want to print.
objects = []

# Loop over every line in the file.
for sentence in all_sentences:

    # Skip blank lines (empty strings after splitting on "\n")
    if not sentence.strip():
        continue

    # Each line is a comma-separated group, e.g.:  ebela,bela,lae,ela,beela
    # The FIRST item is the base word we want to analyse.
    # Split the line on commas to get all words in the group.
    possible_words = sentence.split(",")

    # ── Handle bracketed base words ──────────────────────────────────────────
    # Some lines start with a word in parentheses, e.g.: (ngwaela),ngwae,ela
    # The brackets signal that this word is a constructed/compound form and
    # should NOT count as a "real" word for the game.
    # We use 'begin' to skip it when we build the list of actual game words.

    # Get the raw first word (may have brackets)
    raw_first = possible_words[0]

    if raw_first.startswith("(") and raw_first.endswith(")"):
        begin = 1   # skip the bracketed word; real words start at index 1
    else:
        begin = 0   # no brackets; the first word IS a real game word

    # actual_words = the slice of the list that contains playable game words
    actual_words = possible_words[begin:]

    # ── Clean up the base word ───────────────────────────────────────────────
    # Strip any surrounding brackets from the base word so we can analyse it.
    # .strip("(") removes "(" from left and right.
    # .strip(")") removes ")" from left and right.
    # .strip()    removes any extra whitespace.
    base_word = raw_first.strip("(").strip(")").strip()

    # ── Extract syllables ────────────────────────────────────────────────────
    # Call extract_syllable() with the clean base word.
    # Returns a list like ['e', 'be', 'la'] for "ebela".
    syllables = extract_syllable(base_word)

    # ── Filter by syllable count ─────────────────────────────────────────────
    # If TARGET_SYLLABLE_COUNT is 0 we include everything.
    # Otherwise we only include words whose syllable count matches the target.
    if TARGET_SYLLABLE_COUNT == 0 or len(syllables) == TARGET_SYLLABLE_COUNT:

        # Build a display string:
        #   str(actual_words)  -> "['ebela', 'bela', 'lae', 'ela', 'beela']"
        #   .strip("[").strip("]") -> removes the outer list brackets
        #   + "\t" -> adds a tab character between the words and syllables
        #   str(syllables).strip("[").strip("]") -> same cleanup for syllables
        line = (
            str(actual_words).strip("[").strip("]")
            + "\t"
            + str(syllables).strip("[").strip("]")
        )
        objects.append(line)


# ── Step 4: Print the results ──────────────────────────────────────────────────

# Loop over every formatted result string and print it.
for o in objects:
    print(o)


# ── Step 5: Print a summary ────────────────────────────────────────────────────
print()
if TARGET_SYLLABLE_COUNT == 0:
    print(f"Total words processed: {len(objects)}")
else:
    print(f"Total words with {TARGET_SYLLABLE_COUNT} syllables: {len(objects)}")
