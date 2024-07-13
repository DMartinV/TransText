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
It extracts the textual content of PDF files and saves it into a plain text file. The script uses the 'PyPDF2' library to complete this task. The script first verifies if the input file is a PDF file before starting the extraction process. Once the process is completed, the program adds the textual content into a plain text file.

Usage: $ python function_pdfText.py [-i <pdf_file>] [-o <outputFile>]

Example: $ python function_pdfText.py -i /path/document.pdf -o /path/output.txt
"""
# Import the necessary libraries.
import PyPDF2
import argparse
import os

def isPdfFile(filePath):
    """
    This function checks if the provided path is a PDF file.

    Parameters:
        * filePath (str): Path of the file.

    Returns:
        * bool: True if the file is a PDF file, False if the file is not a PDF.
    """
    # List of the PDF extension.
    pdfExtensions = ['.pdf']
    # Get the extension from the PDF file.
    fileExtension = os.path.splitext(filePath)[1].lower()
    # Check if the extension is on the list.
    return fileExtension in pdfExtensions


def extractTextFromPdf(pdfFile):
    """
    This function extracts text from a PDF file.

    Parameters:
        * pdfFile (str): Path of the input PDF file.

    Returns:
        * str: Extracted text from the PDF.

    Raises:
        * FileNotFound: If the source file is not found.
        * Exception: If an error occurs during the extraction.
    """
    try:
        # If the file exists and if it is a PDF file.
        if os.path.exists(pdfFile) and isPdfFile(pdfFile):
            # Open the PDF file.
            with open(pdfFile, 'rb') as file:
                # Create a PDF Reader object.
                pdfReader = PyPDF2.PdfReader(file)
                # Initialize an empty string to store the extracted text.
                text = ""
                
                # Iterate over all the pages of the PDF.
                for pageNum in range(len(pdfReader.pages)):
                    # Get the current page object.
                    page = pdfReader.pages[pageNum]
                    # Extract text from the page.
                    text += page.extract_text() if page.extract_text() else ""
            # Return the extracted text.
            return text
        # If the file does not exist or the file is not a PDF, the program displays an error message.
        else:
            raise Exception(f'Entry file "{pdfFile}" is not a valid PDF file.')
    # Handle file not found error and shows error message.
    except FileNotFoundError:
        raise FileNotFoundError(f'Source file "{pdfFile}" not found.')
    # Handle other types of errors and shows error message.
    except Exception as e:
        raise Exception(e)

def saveText(text, outputFile):
    """
    This function saves the extracted text into a specified output file.

    Parameters:
        * text (str): Extracted text.
        * outputFile (str): Path of the output file.

    Returns:
        * None.

    Raises:
        * Exception: If an error occurs during the extraction.
    """
    # Execute try/except block
    try:
        # Open the PDF file and write the content into an output file.
        with open(outputFile, 'w', encoding ='utf-8') as finalFile:
            finalFile.write(text)
        # Print sucess message.
        print(f'The conversion was a success! File: "{os.path.basename(outputFile)}" is saved in: "{os.path.abspath(outputFile)}"')
    # Handle other types of errors and print ann error message.
    except Exception as e:
        print(f'Error: {e}')

if __name__ == "__main__":
    """
    Main execution block.
    This block parses command-line arguments to extract the content of a PDF file to a plain text file.
    It requires the path to the PDF file and optionally the path to the output file.
    """
    # Create and configure the arguments parser.
    parser = argparse.ArgumentParser(description='Program to extract text from a PDF file.')
    parser.add_argument('-i', '--input', dest='pdfFile', help='Path to the PDF file', required=True)
    parser.add_argument('-o', '--output', help='Path to the output text file')

    # Parse the arguments previously defined.
    args = parser.parse_args()

    # Execute try/except block
    try:
        # Extract text from the PDF file.
        text = extractTextFromPdf(args.pdfFile)
        # If the user provides the name of the output file in the arguments.       
        if args.output:
            outputFile = args.output
        # If not, the program provides a default output name.
        else:
            # Get the source PDF's absolute path.
            inputDir = os.path.dirname(os.path.abspath(args.pdfFile))
            # Obtain the name of the file without the extension.
            baseName = os.path.splitext(os.path.basename(args.pdfFile))[0]
            # Create the default name by appending the file's base name with "_output.txt"
            outputFile = os.path.join(inputDir, f"{baseName}_output.txt")
        
        # If the process is successful, save the extracted text to the output file.
        if text:
            saveText(text, outputFile)
        # If not, prints an error message.
        else:
            print("Failed to extract text from the PDF file.")
    # Handle other types of errors and shows error message.
    except Exception as e:
        print(f"Error: {e}")
