#    function_pdfText
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
It extracts the textual content of PDF files and saves it into a plain text file. The script uses the 'PyPDF2' library to complete this task. The function 'extractTextFromPdf' iterates through the PDF's pages, extracting the content and writing it into a plain text file.

Usage: $ python function_pdfText.py [-i <pdf_file>] [-o <outputFile>]

Example: $ python function_pdfText.py -i /path/document.pdf -o /path/output.txt
"""

# Imports necessary libraries.
import PyPDF2
import argparse
import os

def extractTextFromPdf(pdfFile, outputPath):
    """
    This function extracts text from a PDF and saves it onto a plain text file.

    Args:
        * pdfFile (str): Path of the input PDF file.
        * outputPath (str): Path of the output file.

    Raises:
        * FileNotFoundError: If the source file is not found.
        * Exception: If an error occurs during the conversion.

    Returns:
        * None.
    """
    # ExecuteS try/except block.
    try:
        # Opens the PDF file.
        with open(pdfFile, 'rb') as file:
            # Create a PDF Reader object.
            pdfReader = PyPDF2.PdfReader(file)
            
            # Initialize an empty string to store the extracted text.
            text = ""
            
            # Iterates over all the pages of the PDF.
            for pageNum in range(len(pdfReader.pages)):
                # Gets the current page object
                page = pdfReader.pages[pageNum]
                
                # Extracts text from the page.
                text += page.extract_text() if page.extract_text() else ""
        
        # Ensures the output directory exists.
        outputDir = os.path.dirname(outputPath)
        if outputDir and not os.path.exists(outputDir):
            os.makedirs(outputDir)

        # Saves the extracted text to a plain text file.
        with open(outputPath, 'w', encoding='utf-8') as outputFile:
            outputFile.write(text)

        # Prints success message.
        print(f'The conversion was a success! File: "{os.path.basename(outputPath)}" is saved in: "{os.path.abspath(outputPath)}"')

    # Handles file not found error.
    except FileNotFoundError:
        print(f'Error: Source file "{pdfFile}" not found.')
    
    # Handles other types of errors.
    except Exception as e:
        print(f'Error: {e}')    

if __name__ == "__main__":
    """
    Main execution block.
    This block parses command-line arguments to extract the content of a PDF file to a plain text file.
    It requires the path to the PDF file and optionally the path to the output file.
    """
    # Configures the argument parser.
    parser = argparse.ArgumentParser(description='Program to extract text from a PDF file.')
    parser.add_argument('-i', '--input', dest='pdfFile', help='Path to the PDF file', required=True)
    parser.add_argument('-o', '--output', dest='outputPath', help='Path to the output text file')
    
    # Parses the arguments.
    args = parser.parse_args()

    # Determines the output path.
    if args.outputPath:
        outputPath = args.outputPath
    else:
        # Creates default output file name based on input file name.
        baseName, _ = os.path.splitext(args.pdfFile)
        outputPath = baseName + '_output.txt'
    
    # Extracts text from the PDF and save it to the specified text file.
    extractTextFromPdf(args.pdfFile, outputPath)

