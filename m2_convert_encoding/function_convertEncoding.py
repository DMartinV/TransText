#    function_convertEncoding
#    Copyright (C) 2023  Diana Martin
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
This script serves as the functional aspect of this module.
It provides two main functions for converting file encodings. The former detects the file's encoding with the use of the 'chardet' library. The latter converts the file into the desired encoding.

Usage: $ python function_convertEncoding.py <sourceFile> -e <outputEncoding> [-o <outputFile>]

Example: $ python function_convertEncoding.py /path/file.txt -e utf-8 -o /path/output/file.txt
"""

# Import necessary libraries.
import argparse
import codecs
import chardet
import os

def detectEncoding(inputFile):
    """
    This function detects the character encoding of a file.

    Parameters:
        * inputFile (str): Path of the input file.

    Returns:
        str: Character encoding of the input file.
    """

    # Open and read the entry file (in binary data).
    rawData = open(inputFile, "rb").read()

    # Detect the file's encoding.
    encoding = chardet.detect(rawData)

    # Return the encoding
    return encoding["encoding"]

def convertEncoding(sourceFile, outputEncoding, outputFile=None):
    """
    This function convertS the character encoding of a file.

    Parameters:
        * sourceFile (str): Path of the source file.
        * outputEncoding (str): Encoding of the output file.
        * outputFile (str, optional): Path of the output file after the conversion.

    Returns:
        * None.

    Raises:
    * FileNotFoundError: If the source file is not found.
    * Exception: If an error occurs during the conversion.
    """
    # Execute try/except block
    try:
        # Detect the encoding of the input file.
        sourceEncoding = detectEncoding(sourceFile)

        # If the source and the output files have the same encoding, no conversion is needed.
        if sourceEncoding == outputEncoding:
            print("The input file and output file have the same encoding. No conversion needed.")
            return
        
        # Open the content of the source file and read its content.
        with codecs.open(sourceFile, 'r', encoding=sourceEncoding, errors='replace') as originalFile:
            content = originalFile.read()
        
        # If users have not provided a name for the output file, the program generates the following default name.
        if outputFile is None:
            outputFile = os.path.splitext(sourceFile)[0] + "_" + outputEncoding + ".txt"

        # Write the content of the output file into the desired encoding.
        with codecs.open(outputFile, 'w', encoding=outputEncoding, errors='replace') as finalFile:
            finalFile.write(content)

        # Print success message.        
        print(f'The conversion was a success!. File: "{outputFile}" has been converted to "{outputEncoding}" encoding.')
        
        # Print output file's new path.
        print(f'File: "{outputFile}" is saved in: "{os.path.abspath(outputFile)}"')
    
    # Handle file not found error.
    except FileNotFoundError:
        print(f'Error: Source file "{sourceFile}" not found.')
    
    # Handle other types of errors.
    except Exception as e:
        print(f'Error: {e}')

if __name__ == "__main__":
    """
    Main execution block.
    This block parses command-line arguments to convert a file's encoding to another.
    It requires the source file, the output encoding and optionally the output file
    """
    # Create the argument parser.
    parser = argparse.ArgumentParser(description='Program to convert the character encoding of a file.')
    
    # Define the required arguments parser.
    parser.add_argument('-i', '--input', dest='sourceFile', help='Route of the source file.', required=True)
    parser.add_argument('-e', '--outputEncoding', help='Encoding of the output file.', required=True,)
    parser.add_argument('-o', '--outputFile', help='Route of the output file after the conversion.')

    # Parser the arguments previously defined.
    args = parser.parse_args()

    # Convert the file's encoding.
    convertEncoding(args.sourceFile, args.outputEncoding, args.outputFile)

