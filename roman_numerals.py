def to_roman(number):
    roman_numerals = {1: 'I', 5: 'V'}
    return roman_numerals.get(number, "")
