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

def extensionCheck(filePath):
    """
    This function verifies if the provided file path has an acceptable extension.

    Parameters:
        * filePath (str): Path of the file.

    Returns:
        * bool: True if the file extension is in the allowed list, False otherwise.
    """
    # List of extensions allowed in this program.
    extensions = ['.epub', '.eml', '.msg', '.html', '.htm', '.json', '.pptx', '.doc', '.docx', '.odt', '.rtf']
    # Obtain the file extension from the file path.
    fileExtension = os.path.splitext(filePath)[1].lower()
    # Verify that the file extension is on the list.
    return fileExtension in extensions

def extractTextFromFile(inputFile):
    """
    This function extracts text from a file.

    Parameters:
        * inputFile (str): Path of the input file.

    Returns:
        * str: Extracted text from the file.

    Raises:
        * FileNotFoundError: If the source file is not found.
        * Exception: If an error occurs during the conversion.
    """
    # Check if the file extension is supported
    if not extensionCheck(inputFile):
        raise Exception(f'Entry file "{inputFile}" cannot be converted. Unsupported file type.')

    # Execute try/except block
    try:
        # Verify if the source path exists
        if os.path.exists(inputFile):
            # Extract the textual content of the source file.
            text = textract.process(inputFile).decode('utf-8')
            # Return the content.
            return text
        else:
            raise FileNotFoundError(f'Source file "{inputFile}" not found.')
    # Handles other types of errors.
    except Exception as e:
        raise Exception(e)

def saveText(text, outputFile):
    """
    This function saves extracted text to a specified output file.

    Parameters:
        * text (str): Text to be saved.
        * outputFile (str): Path of the output file.

    Returns:
        * None
    
    Raises:
        * Exception: If an error occurs during the extraction.
    """
    # Execute try/except block
    try:
        # Open the source file and write the content onto the output file.
        with open(outputFile, 'w', encoding='utf-8') as finalFile:
            finalFile.write(text)
        # Print success message.  
        print(f'The conversion was a success! File: "{os.path.basename(outputFile)}" is saved in: "{os.path.abspath(outputFile)}"')
    # Handle other types of errors.
    except Exception as e:
        print(f'Error: {e}')

if __name__ == "__main__":
    """
    Main execution block.
    This block parses command-line arguments to extract the content of a file to a plain text file.
    It requires the path to the input file and optionally the path to the output file.
    """
    # Configure the arguments parser.
    parser = argparse.ArgumentParser(description='Program to extract text from various types of files.')
    parser.add_argument('-i', '--input', dest='inputFile', help='Path to the input file', required=True)
    parser.add_argument('-o', '--output', help='Path to the output text file')
    
    # Parse the arguments previously defined.
    args = parser.parse_args()

    # Execute try/except block
    try:
        # Check file extension
        if not extensionCheck(args.inputFile):
            raise Exception(f'Entry file "{args.inputFile}" cannot be converted. Unsupported file type.')
        
        # Extract text from the input file.
        text = extractTextFromFile(args.inputFile)

        # If the user provides the name of the output file in the arguments.       
        if args.output:
            outputFile = args.output
        # If not, the program provides a default output name.
        else:
            # Get the source file's absolute path. 
            inputDir = os.path.dirname(os.path.abspath(args.inputFile))
            # Obtain the name of the file without the extension.
            baseName = os.path.splitext(os.path.basename(args.inputFile))[0]
            # Create the default name by appending the file's base name with "_output.txt"
            outputFile = os.path.join(inputDir, f"{baseName}_output.txt")
        
        # If the process is successful, save the extracted text to the output file.
        if text:
            saveText(text, outputFile)
        # If not, print an error message.
        else:
            print("Failed to extract text from the file.")
    
    # Handle other types of errors and show message.
    except Exception as e:
        print(f"Error: {e}")
