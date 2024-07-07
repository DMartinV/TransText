#    function_imageText
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
It extracts text from different types of image files using OCR (Optical Character Recognition). The script processes the file using the 'textract' library to decode and extract the text from the image. The user can also specify the language of the source image (it is recommended). If the language is not specified, it defaults to English. The script also includes a function with a list of language codes supported by the library. Furthermore, this script handles errors, including checking for the existence of the file, etc.

Usage: $ python function_imageText.py -i <image_path> [-l <language_code>] [-o <output_file>]

Example: $ python function_imageText.py -i /path/image.jpg -l eng -o /path/output.txt
"""

# Imports necessary libraries.
import argparse
import os
import textract

def extractTextFromImage(imagePath, language=None):
    """
    Extracts text from an image file.

    Args:
        * imagePath (str): Path of the image file.
        * language (str, optional): Language code. If specified, the OCR will perform the extraction according to the specified language.

    Raises:
        * Exception: If an error occurs during the conversion.

    Returns:
        * str or None: Extracted text if successful, None otherwise.
    """
    # Executes try/except block.
    try:
        # Verifies if the source path exists.
        if os.path.exists(imagePath):
            # If source exists, it checks for a specified language.
            if language:
                text = textract.process(imagePath, language=language)
            # Extracts without specifying the language. It will use the default language (English).
            else:
                text = textract.process(imagePath)
            # Decodes the string to 'UTF-8' and returns it.
            return text.decode('utf-8')
         # If the source path doesn't exist, then an error message is displayed in the console.
        else:
            print(f'Error: Entry file "{imagePath}" does not exist.')
            return None
    # Handles other types of errors.
    except Exception as e:
        print(f'Error: {e}')
        return None

def getLanguageCodes():
    """
    Gets a list of language codes commonly used in OCR.

    Returns:
        list: List of language codes.
    """
    # List that contains language codes.
    languageCodes = [
        "afr", "amh", "ara", "aze", "bel", "ben", "bos", "bul", "cat", "ceb", 
        "ces", "chi_sim", "chi_tra", "cym", "dan", "deu", "ell", "eng", "epo", 
        "est", "eus", "fas", "fin", "fra", "gle", "glg", "guj", "hat", "hau", 
        "heb", "hin", "hrv", "hun", "hye", "ind", "isl", "ita", "jav", "jpn", 
        "kan", "kat", "kaz", "khm", "kir", "kor", "kur", "lao", "lat", "lav", 
        "lit", "ltz", "mal", "mar", "mkd", "mlg", "mlt", "mon", "msa", "mya", 
        "nep", "nld", "nor", "nya", "pan", "pol", "por", "pus", "ron", "rus", 
        "sin", "slk", "slv", "snd", "som", "spa", "sqi", "srp", "sun", "swa", 
        "swe", "tam", "tel", "tgk", "tgl", "tha", "tur", "ukr", "urd", "uzb", 
        "vie", "xho", "yor", "zho", "zul"
    ]
    return languageCodes

def saveText(text, outputFile):
    """
    Saves extracted text to a specified output file.

    Args:
        * text (str): Text to be saved.
        * outputFile (str): Path of the output file.

    Returns:
        * None
    """
    # Executes try/except block.
    try:
        # Saves the extracted text to a plain text file.
        with open(outputFile, 'w', encoding='utf-8') as finalFile:
            finalFile.write(text)
        # Prints success message.
        print(f'The conversion was a success! File: "{os.path.basename(outputFile)}" is saved in: "{os.path.abspath(outputFile)}"')
    # Handles other types of errors.
    except Exception as e:
        print(f'Error: {e}')

if __name__ == "__main__":
    """
    Main execution block.
    This block parses command-line arguments to extract text from an image file and optionally save it to an output file.
    """
    
    # Creates the argument parser.
    parser = argparse.ArgumentParser(description='Program to extract text from an image file.')
    parser.add_argument('-i', '--input', dest='imagePath', help='Path of the input image file.', required=True)
    parser.add_argument('-l', '--language', help='Language code for OCR.', required=False)
    parser.add_argument('-o', '--output', dest='outputFile', help='Path of the output text file.', required=False)

    # Parses the arguments previously defined.
    args = parser.parse_args()

    # Extracts text from the input file.
    text = extractTextFromImage(args.imagePath, args.language)
    
    # Determines the output file name.
    if args.outputFile:
        output_file = args.outputFile
    else:
        # Generates output file name.
        base_name = os.path.splitext(os.path.basename(args.imagePath))[0]
        output_file = f"{base_name}_output.txt"

    # Saves the extracted text to the output file if provided.
    if text:
        saveText(text, output_file)
    else:
        print("Failed to extract text from the image file.")
