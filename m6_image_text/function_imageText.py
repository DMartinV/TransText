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
It extracts text from different types of image files using OCR (Optical Character Recognition). The script processes the file using the 'pytesseract' library to decode and extract the text from the image. The user can also specify the language of the source image (it is recommended). If the language is not specified, it defaults to English. The script also includes a function with a list of language codes supported by the library. Furthermore, this script handles errors, including checking for the existence of the file, etc.

Usage: $ python function_imageText.py -i <image_path> [-l <language_code>] [-o <output_file>]

Example: $ python function_imageText.py -i /path/image.jpg -l eng -o /path/output.txt

"""
# Import the necessary libraries.
import os
import argparse
import pytesseract
from PIL import Image

def extractTextFromImage(pathSource, language=None):
    """
    This function extracts the textual content from an image file.

    Parameters:
        * pathSource (str): Path of the image file.
        * language (str, optional): Language code. it is highly recommended to specify the language to perform a better extraction.

    Returns:
        * str or None: Extracted text if successful, None otherwise.
    """
    # Execute try/except block.
    try:
        # Verify if the source path exists.
        if os.path.exists(pathSource):
            # Open the image imported into the program.
            img = Image.open(pathSource)
            # If source exists and is an image, it checks for a specified language.
            if language:
                # Extract text with the specified language.
                text = pytesseract.image_to_string(img, lang=language)
            else:
                # Extract text with the default language (English).
                text = pytesseract.image_to_string(img)
            # Return the extracted content.
            return text
        # If the source path does not exist, then show an error message.
        else:
            print("Error", "Entry file does not exist.")
            return None
    # Handle other types of errors and show an error message.
    except Exception as e:
        print("Error", f"An error occurred: {e}")
        return None

def saveText(text, outputFile):
    """
    This function saves the extracted text to a specified output file.

    Parameters:
        * text (str): Text to be saved.
        * outputFile (str): Path of the output text file.

    Returns:
        * None.
    """
    # Execute try/except block.
    try:
        # Save the extracted text into a plain text file.
        with open(outputFile, 'w', encoding='utf-8') as file:
            file.write(text)
        # Print success message.
        print(f"Text saved successfully to: {outputFile}")
    # Handle other types of errors and print error message.
    except Exception as e:
        print(f"Error: Failed to save text to {outputFile}. Error: {e}")

def getLanguageCodes():
    """
    This function gets a list of language codes commonly used in OCR.

    Returns:
    - list: List of language codes.
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

if __name__ == "__main__":
    """
    Main execution block.
    This block parses command-line arguments to extract text from an image file and optionally save it to an output file.
    """
    # Create the argument parser.
    parser = argparse.ArgumentParser(description='Program to extract text from an image file.')
    parser.add_argument('-i', '--input', dest='imagePath', help='Path of the input image file.', required=True)
    parser.add_argument('-l', '--language', help='Language code for OCR.', required=False)
    parser.add_argument('-o', '--output', dest='outputFile', help='Path of the output text file.', required=False)

    # Parse the arguments previously defined.
    args = parser.parse_args()

    # Extract text from the input image file.
    text = extractTextFromImage(args.imagePath, args.language)

    # Execute try/except block
    try:
        # Determine the output's file name.
        if args.outputFile:
            outputFile = args.outputFile
        else:
            # Generate output file name in the same directory as the input file.
            inputDir = os.path.dirname(os.path.abspath(args.imagePath))
            baseName = os.path.splitext(os.path.basename(args.imagePath))[0]
            outputFile = os.path.join(inputDir, f"{baseName}_output.txt")

        # If the process is successful, save the extracted text to the output file.
        if text:
            saveText(text, outputFile)
        # If not, print an error message.
        else:
            print("Failed to extract text from the image file.")
    # Handle other types of errors and show message.
    except Exception as e:
        print(f"Error: {e}")
