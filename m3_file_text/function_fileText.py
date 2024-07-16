#    function_fileText
#    Copyright (C) 2024  Diana Martin
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
It extracts the textual content of various types of files and saves it into a plain text file. The script uses the 'textract' library to complete this task. The script first checks the extension of the file before extracting the text and saving it into a plain text file.

Usage: $ python function_fileText.py <file> [-o <outputFile>]

Example: $ python function_fileText.py /path/document.docx -o /path/output.txt
"""
# Import necessary libraries.
import textract
import argparse
import os

def extractTextFromFile(inputFile, outputPath):
    """
    This function extracts text from a file and saves it to a plain text file.

    Args:
        * inputFile (str): Path of the input file.
        * outputPath (str): Path of the output file.

    Raises:
        * FileNotFoundError: If the source file is not found.
        * Exception: If an error occurs during the conversion.

    Returns:
        * None.
    """
    # Execute try/except block
    try:
        # Extract text from the file using textract
        text = textract.process(inputFile)
        
        # Convert bytes to string
        text = text.decode('utf-8')

        # Save the extracted text to a plain text file
        with open(outputPath, 'w', encoding='utf-8') as outputFile:
            outputFile.write(text)

        # Print success message.        
        print(f'The conversion was a success! File "{os.path.basename(outputPath)}" is saved in: "{os.path.abspath(outputPath)}"')
    
    # Handle file not found error.
    except FileNotFoundError:
        print(f'Error: Source file "{inputFile}" not found.')
    
    # Handle other types of errors.
    except Exception as e:
        print(f'Error: {e}')

if __name__ == "__main__":
    """
    Main execution block.
    This block parses command-line arguments to extract the content of a file to a plain text file.
    It requires the path to the input file and optionally the path to the output file.
    """
    # Configure the argument parser
    parser = argparse.ArgumentParser(description='Program to extract text from various types of files.')
    parser.add_argument('-i', '--input', dest='inputFile', help='Path to the input file', required=True)
    parser.add_argument('-o', '--output', help='Path to the output text file')

    # Parse the arguments
    args = parser.parse_args()

    # Determine the output path
    if args.output:
        outputPath = args.output
    else:
        # Create default output file name based on input file name
        baseName, _ = os.path.splitext(args.inputFile)
        outputPath = baseName + '_output.txt'

    # Extract text from the file and save it to the specified text file
    extractTextFromFile(args.inputFile, outputPath)
