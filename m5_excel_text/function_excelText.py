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
It extracts the textual content of Excel files and saves it into a plain text file. The script uses the 'openpyxl' library to complete this task. The program first verifies if the extension provided is from an Excel file before extracting the text and saving it into a plain text file.

Usage: $ python function_excelText.py [-i <excel_file>] [-o <outputFile>]

Example: $ python function_excelText.py -i /path/document.xlsx -o /path/output.txt
"""
# Import the necessary libraries.
import openpyxl
import argparse
import os

def isExcelFile(filePath):
    """
    This function verifies if the provided file path is an Excel file.

    Parameters:
        * filePath (str): Path of the file.

    Returns:
        * bool: True if the file is an Excel file, False if the file is not an Excel file.
    """
    # List of possible Excel extensions.
    excelExtensions = ['.xls', '.xlsx', '.xlsm', '.xlsb', '.odf', '.ods']
    # Obtain the extension from the source file.
    fileExtension = os.path.splitext(filePath)[1].lower()
    # Check if the extension is on the list.
    return fileExtension in excelExtensions

def extractTextFromExcel(excelPath):
    """
    This function extracts text from an Excel file.

    Parameters:
        * excelPath (str): Path to the input Excel file.

    Returns:
        * str: Extracted text from the Excel file.

    Raises:
        * FileNotFound: If the source file is not found.
        * Exception: If an error occurs during the extraction.    
    """
    # Execute try/except block
    try:
        # If the file exists and it is a Excel file.
        if os.path.exists(excelPath) and isExcelFile(excelPath):
            # Open the Excel file.
            wb = openpyxl.load_workbook(excelPath)
            # Select the first sheet.
            sheet = wb.active
            # Initialize an empty string to store the extracted text.
            text = ""

            # Iterate over all the rows from the Excel sheet.
            for row in sheet.iter_rows():
                # Create a list of cell values as strings, using an empty string for any None values.
                rowData = [str(cell.value) if cell.value is not None else '' for cell in row]
                # Join the list of cell values with a tab delimiter and add the resulting string to the acumulator variable.
                text += '\t'.join(rowData) + '\n'
            # Return the extracted text.
            return text
        
        # If the file does not exist or is not an Excel file, show an error message.
        else:
            raise Exception(f'Entry file "{excelPath}" is not a valid Excel file.')
    # Handle file not found error and display an error message.
    except FileNotFoundError:
        raise FileNotFoundError(f'Source file "{excelPath}" not found.')
    # Handle other types of errors and display an error message.
    except Exception as e:
        raise Exception(e)

def saveText(text, outputFile):
    """
    This function saves the extracted text into a specified output file.

    Parameters:
        * text (str): Text to be saved.
        * outputFile (str): Path of the output file.

    Returns:
        * None.

    Raises:
        * Exception: If an error occurs during the extraction.
    """
    # Execute try/except block.
    try:
        # Open the output file and write the content onto it.
        with open(outputFile, 'w', encoding='utf-8') as finalFile:
            finalFile.write(text)
        # Print success message.
        print(f'The conversion was a success! File: "{os.path.basename(outputFile)}" is saved in: "{os.path.abspath(outputFile)}"')
    # Handle other types of errors and print an error message.
    except Exception as e:
        print(f'Error: {e}')

if __name__ == "__main__":
    """
    Main execution block.
    This block parses command-line arguments to extract the content of an Excel file to a plain text file.
    It requires the path to the Excel file and optionally the path to the output file.
    """  
    # Create and configure the arguments parser.
    parser = argparse.ArgumentParser(description='Program to extract text from an Excel file.')
    parser.add_argument('-i', '--input', dest='excelPath', help='Path to the input Excel file', required=True)
    parser.add_argument('-o', '--output', help='Path to the output text file')

    # Parse the arguments previously defined.
    args = parser.parse_args()

    # Execute try/except block
    try:
        # Extract text from the Excel file.
        text = extractTextFromExcel(args.excelPath)
        # If the user provides the name of the output file in the arguments.       
        if args.output:
            outputFile = args.output
        # If not, the program provides a default output name.
        else:
            # Get the source Excel's absolute path.
            inputDir = os.path.dirname(os.path.abspath(args.excelPath))
            # Obtain the name of the file without the extension.
            baseName = os.path.splitext(os.path.basename(args.excelPath))[0]
            # Create the default name by appending the file's base name with "_output.txt"
            outputFile = os.path.join(inputDir, f"{baseName}_output.txt")

        # If the process is successful, save the extracted text to the output file.
        if text:
            saveText(text, outputFile)
        # If not, print an error message.
        else:
            print("Failed to extract text from the Excel file.")
    # Handle other types of errors and show an error message.
    except Exception as e:
        print(f"Error: {e}")
