#    function_excelText
#    Copyright (C) 2024  Diana Martin Vilá
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
It extracts the textual content of Excel files and saves it into a plain text file. The script uses the 'openpyxl' library to complete this task. The function 'extractTextFromExcel' iterates through the Excel's rows and cells, extracting the content and writing it into a plain text file.

Usage: $ python function_excelText.py [-i <excel_file>] [-o <outputFile>]

Example: $ python function_excelText.py -i /path/document.xlsx -o /path/output.txt
"""

# Imports necessary libraries.
import argparse
import openpyxl
import os

def extractTextFromExcel(excelPath, outputPath):
    """
    Extracts text from an Excel file and saves it to a plain text file.

    Args:
        * excelPath (str): Path to the input Excel file.
        * outputPath (str): Path to the output text file.

    Raises:
        * FileNotFoundError: If the source file is not found.
        * Exception: If an error occurs during the conversion.

    Returns:
        * None.
    """
    # Executes try/except block.
    try:
        # Opens Excel file.
        wb = openpyxl.load_workbook(excelPath)
        # Selects the first sheet.
        sheet = wb.active

        # Initializes an empty string to store the extracted text.
        text = ""

        # Iterates over all rows and columns of the Excel file.
        for row in sheet.iter_rows():
            for cell in row:
                # Adds the cell value to the text.
                text += str(cell.value) + '\n'

        # Saves the extracted text to a plain text file.
        with open(outputPath, 'w', encoding='utf-8') as outputFile:
            outputFile.write(text)

        # Prints success message.
        print(f'The conversion was a success! File: "{os.path.basename(outputPath)}" is saved in: "{os.path.abspath(outputPath)}"')

    # Handles file not found error.
    except FileNotFoundError:
        print(f'Error: Source file "{excelPath}" not found.')
    
    # Handles other types of errors.
    except Exception as e:
        print(f'Error: {e}')

if __name__ == "__main__":
    """
    Main execution block.
    This block parses command-line arguments to extract the content of an Excel file to a plain text file.
    It requires the path to the Excel file and optionally the path to the output file.
    """
    # Configures the argument parser.
    parser = argparse.ArgumentParser(description='Program to text from an Excel file and save it to a plain text file.')
    parser.add_argument('-i', '--input', dest='excelPath', required=True, help='Path to the input Excel file')
    parser.add_argument('-o', '--output', dest='outputPath', help='Path to the output text file')

    # Parses the command-line arguments.
    args = parser.parse_args()

    # Determines the output path.
    if args.outputPath:
        outputPath = args.outputPath
    else:
        # Creates default output file name based on input file name.
        baseName, _ = os.path.splitext(args.excelPath)
        outputPath = baseName + '_output.txt'

    # Extracts text from the Excel file and saves it to the text file.
    extractTextFromExcel(args.excelPath, outputPath)
