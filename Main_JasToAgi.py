__author__ = 'Ruian'

import JasAgiParser
import JasToAliasConverter
import AliasToAgiConverter


if __name__ == "__main__":
    data_file = input("Enter data file:\n")
    parser = JasAgiParser.Parser(data_file)
    parser_output = parser.interaction_dictionary
    jas_convert = JasToAliasConverter.JasToAliasConverter(parser_output)
    jas_convert_output = jas_convert.interaction_dictionary_alias

    dict_agi = {}
    for key in jas_convert_output.keys():
        if key not in dict_agi.keys():
            agi = AliasToAgiConverter.convert_alias_to_agi(key)
            print(agi)
            if agi == "" and key[0:2].upper() == "AT":
                agi = AliasToAgiConverter.convert_alias_to_agi(key[2:])
            dict_agi[key] = agi

    output_filename = input("Enter output file name:\n")
    output_file = open(output_filename, "w")

    for key in jas_convert_output.keys():
        for value in jas_convert_output[key]:
            print(key, dict_agi[key], value)

            output_file.write(dict_agi[key] + "   " + value + "\n")
    output_file.close()