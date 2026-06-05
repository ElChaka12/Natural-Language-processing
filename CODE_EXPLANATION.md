# Code Explanation: Setswana Syllable Extractor
## Line-by-line explanation for every person who reads this code

---

## FILE 1: `syllable.py`

This file contains the core logic — a function that splits a Setswana word
into its syllables. It can also be run directly to test one word.

---

### The function definition

```python
def extract_syllable(word):
```
**What this does:** Declares a reusable block of code called `extract_syllable`.
It accepts one input (`word`) — a string like `"mosadi"` — and when called,
returns a list of syllables like `['mo', 'sa', 'di']`.

---

### Setting up variables

```python
p = 0
```
A counter for how many syllables have been found. (`p` for "position".)
Not used in the return value but kept for tracking.

```python
lastchar = ""
```
Stores the character from the **previous** loop iteration so we can look back
one step. Starts empty because there is no previous character at the beginning.

```python
s = ""
```
The **syllable buffer** — we build the current syllable one character at a time
here. Every time a syllable is complete, we save it and reset `s` to `""`.

```python
sp = ""
```
The **previous value of `s`** — a snapshot of the buffer before the last
character was added. Used by the special `"ng"` rule to look back two characters.

```python
syllables = []
```
The list we will fill with completed syllables and return at the end.

```python
vowels = ["a", "e", "i", "o", "u"]
```
The five Setswana vowels. Every syllable in Setswana ends with a vowel
(it is a CV language — Consonant + Vowel). This list lets us check whether
any character is a vowel with `c in vowels`.

---

### The main loop

```python
for i in range(len(word)):
```
Loop through every position in the word. `range(len(word))` produces the
numbers `0, 1, 2, ...` up to but not including the length of the word.
So for `"mosadi"` (6 characters) this gives `0, 1, 2, 3, 4, 5`.

```python
    c = word[i:i+1]
```
Pull out the character at position `i`. We write `word[i:i+1]` (a slice)
instead of `word[i]` (an index) because slicing never raises an IndexError
— it returns `""` if `i` is out of range. This is a defensive coding habit.

---

### Handling consonants

```python
    if c not in vowels:
        sp = s
        s  = s + c
```
If the current character is a **consonant** (not in the vowels list):
- Save the current buffer into `sp` before changing it (`sp` = "snapshot of s previous").
- Add the consonant to the buffer `s`.

Example: word = `"bela"`, when `c = "b"`:  
`sp = ""`, `s = "b"`

---

### Handling vowels — completing a syllable

```python
    else:
        if c in vowels:
            s = s + c
            syllables.append(s)
            p += 1
            s = ""
```
If the character IS a vowel, the syllable is now complete:
1. Add the vowel to the buffer → `s` now holds a full syllable (e.g. `"be"`).
2. Append it to the `syllables` list.
3. Increment the counter `p`.
4. Reset `s` to `""` ready for the next syllable.

Note: `if c in vowels` inside the `else` block is redundant — if we're in the
`else`, `c` is already guaranteed to be a vowel. It was written for clarity
but can safely be removed.

---

### Special case 1: The `"ng"` cluster

```python
    if sp == "ng" and c != "w" and c not in vowels:
        syllables.append("ng")
        p += 1
        s = c
```
In Setswana, `"ng"` behaves as a nasal consonant cluster and can stand alone
as a syllable unit. This rule fires when:
- `sp == "ng"` — the two characters before the current one spelled `"ng"`, AND
- `c != "w"` — the current character is NOT `"w"` (because `"ngw"` is a
  combined click consonant and should stay together), AND
- `c not in vowels` — the current character is not a vowel (otherwise the
  vowel-handler above already handled it correctly).

When it fires: save `"ng"` as its own syllable, reset `s` to just the current
consonant `c`.

---

### Special case 2: Lone `"n"` nasal

```python
    if lastchar == "n":
        if c != "g" and c != "y" and c != "w" and c not in vowels:
            syllables.append(sp)
            p += 1
            s = ""
            s = c
```
In Setswana, when `"n"` is followed by most consonants, it acts as a standalone
nasal syllable (like the `"n"` in `"nkape"` or `"ntse"`).

This fires when:
- `lastchar == "n"` — the previous character was `"n"`, AND
- The current character is NOT `"g"`, `"y"`, or `"w"` (those pair with `"n"`
  to form combined sounds: `ng`, `ny`, `nw`), AND
- The current character is NOT a vowel.

When it fires: `sp` holds the lone `"n"` (because `sp` was set to `s` just
before `"n"` was added). Save it as a syllable, then start a new buffer with
the current consonant.

```python
        else:
            if c == "g" and i == len(word) - 1:
                syllables.append(s)
                p += 1
                s = ""
```
Sub-case: if `"n"` IS followed by `"g"` AND we are at the very last character
of the word (the `-ng` suffix used in Setswana present-tense verbs like
`"gorogang"` → going), then save `"ng"` as the final syllable.

`i == len(word) - 1` is the check for "are we on the last character?"

---

### Special case 3: Prenasalised consonants with `"m"`

```python
    if lastchar == "m":
        if c == "m" or c == "p" or c == "b" or c == "h":
            syllables.append(sp)
            p += 1
            s = c
```
Setswana has prenasalised consonants: `mm`, `mp`, `mb`, `mh`.
When an `"m"` is immediately followed by one of these four characters, the `"m"`
before it becomes its own syllable.

- `lastchar == "m"` — the previous character was `"m"`.
- `c` is one of `m`, `p`, `b`, `h` — the prenasalised consonant starters.
- `sp` at this point holds the lone `"m"` from the previous step.

Save `sp` (the lone `"m"`) as a syllable, then start the next syllable with
the current character `c`.

---

### Updating `lastchar`

```python
    lastchar = c
```
At the **end** of every loop iteration, record the current character as `lastchar`
so the next iteration can refer back to it. This must be the very last line
inside the loop so every special case above still sees the OLD `lastchar`.

---

### Return

```python
    return syllables
```
After the loop finishes, return the completed list of syllables.

---

### The `__main__` guard

```python
if __name__ == "__main__":
    word = "atamelane"
    print("The word is: ", word)
    print("The syllables are: ", extract_syllable(word))
```
`__name__` is a special Python variable. When you **run** this file directly
(`python syllable.py`), Python sets `__name__` to the string `"__main__"`,
so this block runs and tests the function on `"atamelane"`.

When **another file imports** this module (`from syllable import extract_syllable`),
Python sets `__name__` to `"syllable"` (the module name) — so this block is
**skipped**. This means importing the module never accidentally triggers the test.

---
---

## FILE 2: `syllable_test_code.py`

This file reads the word-game text file, applies `extract_syllable()` to every
base word, and prints groups that match a chosen syllable count.

---

```python
from syllable import extract_syllable
```
Import the function from `syllable.py`. Python looks for `syllable.py` in the
same folder. After this line, we can call `extract_syllable()` directly.

---

```python
with open("Word game text file.txt", "r") as f:
    all_sentences = f.read().split("\n")
```
- `open(filename, "r")` — opens the file in **read** mode.
- `with ... as f:` — a **context manager**. It automatically closes the file
  when the indented block finishes, even if an error occurs.
- `f.read()` — reads the entire file content as one long string.
- `.split("\n")` — splits that string at every newline character, producing a
  list where each element is one line of the file.

**Why is `f.close()` gone?**  
The original code called `f.close()` manually inside the `with` block. That is
unnecessary — `with` already handles closing. It was harmless but redundant.

---

```python
TARGET_SYLLABLE_COUNT = 5
```
**This is the key fix to the original limitation.**  
The original code had `if len(syllables) == 5:` buried inside the loop — a
"magic number" that was hard to notice and impossible to change without
modifying the logic. Moving it here as a named constant means:
- Set it to `3` → show 3-syllable words.
- Set it to `0` → show ALL words (no filter).
- It is immediately visible at the top of the script.

---

```python
objects = []
```
An empty list. We collect formatted result strings here before printing them
all at the end. (Collecting first and printing last means the output is clean
and not mixed with any processing messages.)

---

```python
for sentence in all_sentences:
```
Loop through every line of the file. Each `sentence` is one comma-separated
group like `"ebela,bela,lae,ela,beela"`.

```python
    if not sentence.strip():
        continue
```
Skip blank lines. `sentence.strip()` removes whitespace; if the result is an
empty string, `not ""` is `True`, so we `continue` to the next line.
This prevents crashes on the empty lines at the end of the file.

---

```python
    possible_words = sentence.split(",")
```
Split the line on commas. For `"ebela,bela,lae,ela,beela"` this gives:
`['ebela', 'bela', 'lae', 'ela', 'beela']`

```python
    raw_first = possible_words[0]
```
The first item in the list is the **base word** (the word whose syllables we
analyse). Store it separately so we can inspect it for brackets.

```python
    if raw_first.startswith("(") and raw_first.endswith(")"):
        begin = 1
    else:
        begin = 0
```
Some lines have a bracketed first word like `"(ngwaela),ngwae,ela,lae"`.
The brackets mean it is a constructed word, not a playable game word.
- If brackets are found, `begin = 1` → skip the first word when we build
  `actual_words`.
- Otherwise `begin = 0` → keep the first word.

```python
    actual_words = possible_words[begin:]
```
Slice the list from `begin` onwards. This is the list of real, playable words
in the group that will appear in the output.

---

```python
    base_word = raw_first.strip("(").strip(")").strip()
```
Clean up the base word for analysis:
- `.strip("(")` — removes any `(` from the left or right edge.
- `.strip(")")` — removes any `)` from the left or right edge.
- `.strip()` — removes any remaining spaces or `\r` (Windows line endings).

We still analyse the base word even if it was bracketed — we just do not
include it in `actual_words`.

---

```python
    syllables = extract_syllable(base_word)
```
Call the imported function. It returns a list of syllable strings.

---

```python
    if TARGET_SYLLABLE_COUNT == 0 or len(syllables) == TARGET_SYLLABLE_COUNT:
```
The filter:
- `TARGET_SYLLABLE_COUNT == 0` → include everything (no filter).
- `len(syllables) == TARGET_SYLLABLE_COUNT` → include only words with the
  exact syllable count we want.

The `or` means either condition being True is enough to proceed.

---

```python
        line = (
            str(actual_words).strip("[").strip("]")
            + "\t"
            + str(syllables).strip("[").strip("]")
        )
        objects.append(line)
```
Build one display string per matching word group:
- `str(actual_words)` converts the list to a string like `"['ebela', 'bela']"`.
- `.strip("[").strip("]")` removes the outer square brackets.
- `"\t"` is a tab character — creates a column gap when printed.
- `str(syllables).strip("[").strip("]")` — same treatment for the syllable list.

The whole thing is appended to `objects` for printing later.

---

```python
for o in objects:
    print(o)
```
Print every collected result. Each line shows the word group and its syllables
separated by a tab.

---

```python
print()
if TARGET_SYLLABLE_COUNT == 0:
    print(f"Total words processed: {len(objects)}")
else:
    print(f"Total words with {TARGET_SYLLABLE_COUNT} syllables: {len(objects)}")
```
Print a summary line after all results.
- `print()` prints a blank line for spacing.
- `f"..."` is an **f-string** — the `{}` parts are filled in with actual values
  at runtime. `len(objects)` gives the count of items in the list.

---

## Summary of bugs fixed

| Problem | Original code | Fixed code |
|---|---|---|
| Only ran on one word | `if __name__ == "__main__":` block in `syllable.py` ran when imported | The `__main__` guard was already correct — the test code **was** reading the file, but results only printed if `len(syllables) == 5` which is easy to miss |
| Hard-coded limit of 5 | `if len(syllables) == 5:` | `TARGET_SYLLABLE_COUNT = 5` variable at the top, easily changed |
| File not closed safely | `f.close()` called manually inside `with` block | Removed — `with` handles this automatically |
| Blank line crashes | No blank line check | `if not sentence.strip(): continue` added |
| Windows line endings | `strip(")")` might leave `\r` | Added `.strip()` after bracket removal |
