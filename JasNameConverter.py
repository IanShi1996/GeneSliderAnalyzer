__author__ = 'Ruian'

import Parser
import re

class JasNameConverter:
    """
    The JasNameConverter class converts an existing dictionary of JASPAR
    names and converts them to their alias, using the BioPython package's
    jaspar module.

    Attributes:
        interaction_dictionary_jas (Dict): A dictionary of JASPAR names and
            their AGI targets

        interaction_dictionary_alias (Dict): A dictionary of alias names and
            their AGI targets. Derived from interaction_dictionary_jas
    """

    def __init__(self, interaction_dictionary):
        """ (JasNameConverter, Dict) -> None
        Initializes the JasNameConverter object

        Args:
            interaction_dictionary (Dict): A dictionary of interactions,
                with JASPAR names as keys, and a list of AGI targets as their
                values
        """

        self.interaction_dictionary_jas = interaction_dictionary
        # Generate alias dictionary from jaspar name dictionary
        self.interaction_dictionary_alias = \
            self.convert_jas_to_alias(interaction_dictionary)

    def convert_jas_to_alias(self, jas_data):
        """ (JasNameConverter, Dictionary) -> Dictionary

        Return a new dictionary constructed from a interaction dictionary of
        jaspar names and AGI targets by replacing the jaspar names with
        aliases.

        Args:
            jas_data (Dict): A dictionary of jaspar names with their
                corresponsing agi targets as a list

        Return:
            A dictionary of aliases with their agi targets
        """
        # Read data from JASPAR database
        jas_file = open("pfm_plants.txt")
        jas_data = jas_file.read()

        new_dict = {}

        for jas_key in self.interaction_dictionary_jas.keys():
            # Regex to find jaspar name, and capture alias
            regex = re.compile(">MA" + jas_key[2:6] + "\.\d (\\b.+)")
            result = regex.search(jas_data)
            # Check if result was found
            if result:
                # Get captured alias
                alias = result.group(1)
                # Add as key in new dictionary, with same AGI targets
                new_dict[alias] = self.interaction_dictionary_jas[jas_key]

        return new_dict

if __name__ == "__main__":
    parser = Parser.Parser("3000.csv.txt")
    test = JasNameConverter(parser.interaction_dictionary)
    print(test.interaction_dictionary_alias.get("MYC4"))