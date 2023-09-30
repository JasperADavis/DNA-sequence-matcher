import csv
import sys


def main():
    # Check for command-line usage
    argc = len(sys.argv)

    if argc != 3:
        sys.exit()

    db_name = sys.argv[1]
    seq_name = sys.argv[2]

    # Read database file into a variable
    # TODO: Redundant?
    with open(db_name, "r") as db_file:
        db = db_file.read()

    try:
        with open(db_name, "r") as db_file:
            db = db_file.read()
    except FileNotFoundError:
        sys.exit("File not found (DB)")

    # Read DNA sequence file into a variable
    try:
        with open(seq_name, "r") as seq_file:
            seq = seq_file.read()
    except FileNotFoundError:
        sys.exit("File not found (DNA Sequence)")

    """
    NOTE - nomenclature for related variables:

    FILEPATH: db_name
    FILE OBJECT: db_file
    FILE CONTENTS (AS STRING): db
    """

    # Find longest match of each STR in DNA sequence
    top_line = db.split("\n", 1)[0]
    people_rows = db.split("\n", 1)[-1]
    STRs_as_string = top_line.split(",", 1)[-1]
    STR_list = STRs_as_string.split(",")
    seq_to_longest = {}

    # Run each STR sequence through specified sequence file
    for i in STR_list:
        seq_to_longest[i] = longest_match(seq, i)

    # Check database for matching profiles
    current_str = None
    current_person = None
    comparison_num = None
    comparison_list = []

    for i in STR_list:
        current_str = i
        comparison_num = seq_to_longest[current_str]
        comparison_list.append(comparison_num)

    list_of_person_rows = people_rows.split("\n")

    for index, row in enumerate(list_of_person_rows):
        row = row.split(",")
        list_of_person_rows[index] = row
    list_of_person_rows.pop(-1)

    for row in list_of_person_rows:
        # NOTE: current_row = element
        for index, element in enumerate(row):
            if index == 0:
                current_person = element
            else:
                if int(element) != comparison_list[index - 1]:
                    current_person = None
                    break
        if current_person:
            break

    if not current_person:
        result = "No match"
    else:
        result = current_person
    print(result)


def longest_match(sequence, subsequence):
    """Returns length of longest run of subsequence in sequence."""

    # Initialize variables
    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)

    # Check each character in sequence for most consecutive runs of subsequence
    for i in range(sequence_length):
        # Initialize count of consecutive runs
        count = 0

        # Check for a subsequence match in a "substring" (a subset of characters) within sequence
        # If a match, move substring to next potential match in sequence
        # Continue moving substring and checking for matches until out of consecutive matches
        while True:
            # Adjust substring start and end
            start = i + count * subsequence_length
            end = start + subsequence_length

            # If there is a match in the substring
            if sequence[start:end] == subsequence:
                count += 1

            # If there is no match in the substring
            else:
                break

        # Update most consecutive matches found
        longest_run = max(longest_run, count)

    # After checking for runs at each character in seqeuence, return longest run found
    return longest_run


main()
