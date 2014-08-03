
# Numtowords

Converts arbitrarily large intgers to English words, using the [John Horton
Conway/Richard Kenneth Guy/Allan Wechsler](https://en.wikipedia.org/wiki/Names_of_large_numbers) extension system.

A binary is provided. The library's interface is rather simple to use, see unit tests for examples.

## Usage Examples

    $ main.py
    usage: main.py [-h] [--format {american,british}]
                   [--basemaxpower BASEMAXPOWER] [--basestandardprefs]
                   [--nocommas]
                   nums [nums ...]

<!-- -->

    $ main.py 123456789012345678901234567890
    one hundred and twenty-three octillion, four hundred and fifty-six septillion, seven hundred and eighty-nine sextillion, twelve quintillion, three hundred and forty-five quadrillion, six hundred and seventy-eight trillion, nine hundred and one billion, two hundred and thirty-four million, five hundred and sixty-seven thousand, eight hundred and ninety

<!-- -->

    $ main.py --basemaxpower 3 1234567890
    one thousand thousand thousand, two hundred and thirty-four thousand thousand, five hundred and sixty-seven thousand, eight hundred and ninety

<!-- -->

    >main.py 1000000000000000000000000000000000000000000000000
    one quinquadecillion

<!-- -->

    > main.py --basestandardprefs 1000000000000000000000000000000000000000000000000
    one quindecillion
