#    function_detectEncoding
#    Copyright (C) 2023  Diana Martin Vilá
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""
This script serves as the fuctional aspect of this module.
It reads the input file in binary mode and uses the library 'chardet' to detect the file's encoding. Finally, the script prints the detected encoding in console.

Usage: $ python function_detectEncoding.py -i <file_path>

Example: $ python function_detectEncoding.py -i /path/file.txt

"""

#Imports necessary libraries.
import chardet
import argparse


def detectEncoding(inputFile):
    """
    Detect the character encoding of a file.

    Args:
        * inputFile (str): Path of the input file.

    Returns:
        * str: Character encoding of the input file.
    """

    # Opens and reads the input file (in binary data)
    rawData = open(inputFile,"rb").read()

    # Detects the encode
    encoding = chardet.detect(rawData)

    # Returns the encoding
    return(encoding["encoding"])

if __name__ == "__main__":
    """
    Main execution block.
    This block parses a command-line argument to detect the encoding of a file.
    It requires the source file. 
    """

    # Creates the argument parser.
    parser = argparse.ArgumentParser(description='Program to detect the character encoding of a file.')
    
    # Define the required argument parser (-i).
    parser.add_argument('-i', '--input', action="store", dest="inputFile", help='The input file.', required=True)

    # Parsers the argument previously defined.
    args = parser.parse_args()
    
    # Uses the argument. 
    encoding=detectEncoding(args.inputFile)
    
    # Prints the detected encoding of the input file.
    print(encoding)
