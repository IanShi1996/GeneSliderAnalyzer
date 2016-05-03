__author__ = 'Ruian'

from splinter import Browser


def convert_alias_to_agi(alias):
    """(String) -> String

    Return an agi which corresponds to a given alias. Queries the BAR _at to
    Agi tool using splinter.
    """
    with Browser() as browser:
        # at to agi tool url
        url = "http://bar.utoronto.ca/ntools/cgi-bin/ntools_agi_converter.cgi"

        browser.visit(url)
        # Selects gene alias conversion
        drop_down = browser.find_by_name("fromList")[0]
        drop_down.select("Gene Alias")
        # Selects option drop down
        browser.find_by_css("body > form > button")[0].click()
        # Selects agi option
        browser.find_by_css("#ui-multiselect-toList-option-0")[0].check()
        # Inputs the user alias
        browser.fill('input', alias)

        # Submits the query
        browser.find_by_css('body > form > '
                            'input[''type="submit"]:nth-child(14)')[0].click()

        # Gets the agi value
        value = browser.find_by_xpath("//*[@id='table_id']/tbody/tr/td[2]")[0]

        return value.text

if __name__ == "__main__":
    user_input = input("Insert alias to query:\n")
    output = convert_alias_to_agi(user_input)
    print(output)
    input("Finished")

