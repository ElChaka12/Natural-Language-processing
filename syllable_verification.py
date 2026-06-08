# Reads "Word game text file.txt", where each line is:
#   base_word, solution1, solution2, ...
# or
#   (base_word), solution1, solution2, ...  (parentheses = base word excluded from solution checks)
#
# Removes any solution word whose syllables are not a subset of the base word's syllables.
# Writes the cleaned lines to "Cleaned Word game text file.txt".

from syllable import extract_syllable

# Load the entire input file and split into individual lines
with open("Word_game_text_file_v2.txt", "r") as f:
    all_sentences = f.read().split("\n")

# Accumulators for the output and summary statistics
cleaned_lines = []
total_removed = 0
total_kept    = 0

# Process each comma-separated line from the input file
for sentence in all_sentences:

    # Skip blank lines
    if not sentence.strip():
        continue

    possible_words = sentence.split(",")
    raw_first = possible_words[0]

    # begin=1 skips the base word when it's parenthesised (it's a label, not a solution)
    if raw_first.strip().startswith("(") and raw_first.strip().endswith(")"):
        begin = 1
    else:
        begin = 0

    # Strip parentheses and whitespace to get the clean base word
    base_word = raw_first.strip("(").strip(")").strip()

    # Skip lines where the base word is missing or contains non-alpha characters
    if not base_word or not base_word.isalpha():
        continue

    # Slice the candidate solutions (skip index 0 if the base is parenthesised)
    actual_words_list = possible_words[begin:]
    base_syllables = extract_syllable(base_word)

    # Skip if the base word has no syllables (unrecognised word)
    if not base_syllables:
        continue

    base_syllable_set = set(base_syllables)
    valid_solution_words = []
    removed_words = []

    # Check each candidate solution against the base word's syllable set
    for word in actual_words_list:
        word = word.strip()

        # Skip empty tokens and non-alphabetic entries
        if not word or not word.isalpha():
            continue

        word_syllables = extract_syllable(word)

        # Skip if the word's syllables cannot be determined
        if not word_syllables:
            continue

        word_syllable_set = set(word_syllables)

        # Keep the word only if all its syllables appear in the base word
        if word_syllable_set.issubset(base_syllable_set):
            valid_solution_words.append(word)
            total_kept += 1
        else:
            extra_syllables = word_syllable_set - base_syllable_set
            print(f"REMOVED '{word}' (from '{base_word}'): "
                  f"syllables {sorted(extra_syllables)} not in base set {sorted(base_syllable_set)}")
            removed_words.append(word)
            total_removed += 1

    # Only write a line if at least one valid solution survived
    if valid_solution_words:
        output_base = f"({base_word})" if begin == 1 else base_word
        cleaned_line = output_base + "," + ",".join(valid_solution_words)
        cleaned_lines.append(cleaned_line)

# Write all surviving lines to the output file
with open("Cleaned Word game text file_v2.txt", "w") as f:
    f.write("\n".join(cleaned_lines))

# Print a final summary of what was kept, removed, and written
print()
print(f"Data cleaning complete.")
print(f"Total valid solution words kept    : {total_kept}")
print(f"Total invalid solution words removed: {total_removed}")
print(f"Lines written to file              : {len(cleaned_lines)}")
print(f"Cleaned data written to 'Cleaned Word game text file.txt'")
