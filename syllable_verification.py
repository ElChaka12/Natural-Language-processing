from syllable import extract_syllable


# This script reads a Setswana word-game text file, 
#separate base words from solution words
# extracts syllables from every base word using the extract_syllable() function,
# extract all syllables from solution words and compare them to the base word syllables
####pass an error message if the solution words do not contain the same syllables as the base wordwith open("Word game text file.txt", "r") as f:##
#return the error message and remove the word from the list of solution words if it does not contain the same syllables as the base word
#return a success message if all solution words contain the same syllables as the base word
#return the cleaned file with only the valid solution words that contain the same syllables as the base word


with open("Word game text file.txt", "r") as f:
    all_sentences = f.read().split("\n")


    cleaned_lines = []
    total_removed = 0
    total_kept    = 0



for sentence in all_sentences:

    # Skip blank lines (empty strings after splitting on "\n")
    if not sentence.strip():
        continue


    possible_words = sentence.split(",")

# Get the raw first word (may have brackets)
    raw_first = possible_words[0]

    if raw_first.startswith("(") and raw_first.endswith(")"):
        begin = 1   # skip the bracketed word; real words start at index 1
    else:
        begin = 0   # no brackets; real words start at index 0


    # Clean up the base word 
    # Strip any surrounding brackets from the base word so we can analyse it.
    # .strip("(") removes "(" from left and right.
    # .strip(")") removes ")" from left and right.
    # .strip()    removes any extra whitespace.

    base_word = raw_first.strip("(").strip(")").strip()

    if not base_word or not base_word.isalpha():
        continue

    actual_words_list = possible_words[begin:]




    # Extract syllables 
    # Call extract_syllable() with the clean base word.
    # Returns a list like ['e', 'be', 'la'] for "ebela".
    base_syllables = extract_syllable(base_word)

    if not base_syllables:
        continue
    print(type(extract_syllable))   # should print <class 'function'>
    base_syllable_set = set(base_syllables)
#iterate through the actual words and extract syllables from each, then compare to base syllables and print an error message and remove the word from the list if it does not contain the same syllables as the base word
    valid_solution_words = []
    removed_words = []

    for word in actual_words_list:
      word = word.strip()  # Remove extra whitespace

    if not word.isalpha():
          continue  # Skip non-alphabetic words
      
    if not word:
          continue  # Skip empty words


    word_syllables = extract_syllable(word)
    if not word_syllables:
          continue  # Skip words that can't be syllable-extracted
      
    word_syllable_set = set(word_syllables)
      
    if word_syllable_set.issubset(base_syllable_set):
          valid_solution_words.append(word)
          total_kept += 1
    else:
           extract_syllable = word_syllable_set - base_syllable_set
           print(f"Error: '{word}' contains syllables {extract_syllable} not in base word '{base_word}'")
           removed_words.append(word)
           total_removed += 1

           if valid_solution_words:
               cleaned_line = f"{base_word}, " + ", ".join(valid_solution_words)
               cleaned_lines.append(cleaned_line)


        #reurn the cleaned file with only the valid solution words that contain the same syllables as the base word

    with open("Cleaned Word game text file.txt", "w") as f:
           f.write("\n".join(cleaned_lines))


    print()
    print(f"Data cleaning complete")
    print(f"Total valid solution words kept: {total_kept}")
    print(f"Total invalid solution words removed: {total_removed}")
    print(f"Cleaned data written to 'Cleaned Word game text file.txt'")



    