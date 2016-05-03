__author__ = 'Ruian'


class ExcelParser:
    """
    Parses Excel files, which have been converted into a tabs delimited format.

    Attributes:
        excel_file_name (String): The name of the tabs delimited file

    """

    def __init__(self, excel_file_name):
        """ (ExcelParser) -> None

        Initialize excel parser object with the target file, and target
        columns.

        Args:
            excel_file_name (String): The name of the tabs delimited file
        """

        self.excel_file_name = excel_file_name

    def scrape_columns(self, target_columns, header=0):
        """ (ExcelParser) -> List of List of String

        Return a list of size self.target_columns, containing lists of the
        values of all cells in each target column.

        Args:
            target_columns (List of int): The target columns to extract
            header (Int): The amount of lines to skip as part of the header.
        Return:
            The list of list of string
        """

        # Open tabs delimited file
        excel_file = open(self.excel_file_name, "r")
        # Skip header
        for num in range(0, header):
            excel_file.readline()

        # List to store results
        results = self.populate_list(len(target_columns))
        # Parse excel file
        curr_line = excel_file.readline()
        # Check for end of doc
        while curr_line:
            # Remove newline from end of line
            curr_line = curr_line.rstrip()
            # Split into columns
            matches = curr_line.split("\t")

            # Check if target columns are valid
            if self.validate_column_number(target_columns, len(matches)):
                for i in range(0, len(target_columns)):
                    results[i].append(matches[target_columns[i]])
            else:
                print("Exception: Target_column exceeds number of matched "
                      "columns")

            curr_line = excel_file.readline()

        excel_file.close()
        return results

    def validate_column_number(self, target_columns, num_matches):
        """ (ExcelParser, List of Int) -> boolean

        Return whether any specific target column exceeds the number of
        matches columns

        Return: True if no target columns exceeds the number of matched ones.
        """

        for target in target_columns:
            if target > num_matches:
                return False
        return True

    def populate_list(self, target_columns):
        """ (ExcelParser, Int) -> List of Lists

        Return a list of size target_column of empty lists to be used in
        storage of parsed data.

        Args:
            target_columns (Int): The number of lists to create
        Return:
            A list of size target_columns, filled with empty lists.
        """

        new_list = []
        for num in range(0, target_columns):
            new_list.append([])
        return new_list

    def write_to_file(self, output_file_name, parsing_result):
        """ (ExcelParser, String, List of List of String) -> None

        Write a file with the results from the parsing results using a tabs
        delimited format.

        Args:
            output_file_name (String): The name of the file to write to.
            parsing_result (List of List of String): The result from this
                classes parsing methods to be written to a file.
        """
        # Oopen file for writing
        output_file = open(output_file_name, "w")

        # Check if parsing result is valid
        if self.validate_result(parsing_result):
            # Write to file in tabs delimited
            for i in range(0, len(parsing_result[0])):
                output_line = parsing_result[0][i]
                for j in range(1, len(parsing_result)):
                    output_line += ("\t" + parsing_result[j][i])
                output_file.write(output_line + "\n")

        else:
            print("Parsing results may contain errors. Check again.")

    def validate_result(self, parsing_result):
        """ (ExcelParser, List of List of String) -> boolean

        Return whether the parsing result is of even length.

        Args:
            parsing_result (List of List of String): The result from this
                classes parsing methods
        Return:
            True if lengths are even
        """
        length = len(parsing_result[0])

        for i in range(0, len(parsing_result)):
            if len(parsing_result[i]) != length:
                return False
        return True

if __name__ == "__main__":
    target_file = input("Enter data file: \n")
    excel_parser = ExcelParser(target_file)
    output_file = input("Enter output file name:\n")
    target_columns = []
    isDone = False
    while not isDone:
        target_columns.append(int(input("Enter target column:\n")))
        isDone = input("Done?(True/False)\n") == "True"
    header = int(input("Input header count: \n"))
    excel_parser.write_to_file(output_file,
                               excel_parser.scrape_columns(target_columns,
                                                           header))


