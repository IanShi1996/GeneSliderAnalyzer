__author__ = 'Ruian'

import re

class Parser:
    """
    The Parser class parses text files with to retrieve JASPAR names and their
    targets which are in an AGI format. Information is stored in a dictionary,
    with the JASPAR names as keys and AGI targets as values.

    Attributes:
        text_file (File): The file which is opened for further reading and
            parsing of information
        interaction_dictionary (Dict): The dictionary of interactions with
            JASPAR names as keys, and AGI targets as values.
    """

    def __init__(self, file):
        """(Parser, file) -> None

        Initializes the parser module by opening the file.

        Args:
            text_file (File): A text file, with JASPAR names and AGI targets
        """
        # Open file for reading
        self.text_file = open(file, "r")
        # Initialize interaction dictionary
        self.interaction_dictionary = {}
        # Parser data file
        self.parse_data_set()
        # Close reading file
        self.text_file.close()

    def parse_data_set(self):
        """(Parser) -> None

        Parses the data file to obtain a dictionary of JASPAR names and AGI
        targets.
        """

        # Regex to find JASPAR and AGI
        regex = re.compile("(MA\d\d\d\d\.1).(AT\dG\d\d\d\d\d)")
        # Reads all lines
        for line in self.text_file:
            # Find JASPAR and AGI target in current line
            result = regex.match(line)

            # Get JASPAR and AGI if match found
            if result:
                name_jas = result.group(1)
                name_agi = result.group(2)

                # Check if JASPAR name key exists in dictionary
                if name_jas in self.interaction_dictionary:
                    # Appends agi target to list
                    self.interaction_dictionary[name_jas].append(name_agi)
                else:
                    # Creates a new list of agi targets
                    self.interaction_dictionary[name_jas] = [name_agi]

if __name__ == "__main__":
    parser = Parser("3000.csv.txt")
    print((parser.interaction_dictionary.keys()))