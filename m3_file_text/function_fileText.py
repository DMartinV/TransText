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
This script extracts the textual content of various file types and saves it into a plan text file. This program uses several libraries, which are as follows:
    * pptx:
    * docx:
    * bs4:
    * ebooklib:
    * zipfile:

Usage: $ python function_fileText.py <inputFile> [-o <outputFile>]

Example: $ python function_fileText.py /path/document.docx -o /path/output.txt
"""
import argparse
import os
import json
from pptx import Presentation
from docx import Document
from bs4 import BeautifulSoup
import ebooklib
from ebooklib import epub
import zipfile

def is_epub(file_path):
    return file_path.endswith('.epub')

def is_html(file_path):
    return file_path.endswith('.html') or file_path.endswith('.htm')

def is_json(file_path):
    return file_path.endswith('.json')

def is_pptx(file_path):
    return file_path.endswith('.pptx')

def is_docx(file_path):
    return file_path.endswith('.docx')

def is_odt(file_path):
    return file_path.endswith('.odt')

def extract_text_from_epub(file_path):
    book = epub.read_epub(file_path)
    texts = []
    for item in book.get_items():
        if item.get_type() == ebooklib.ITEM_DOCUMENT:
            texts.append(item.get_body_content().decode('utf-8'))
    return '\n'.join(texts)

def extract_text_from_html(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')
        return soup.get_text()

def extract_text_from_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
        return str(data)

def extract_text_from_pptx(file_path):
    prs = Presentation(file_path)
    text_runs = []
    for slide in prs.slides:
        for shape in slide.shapes:
            if hasattr(shape, 'text'):
                text_runs.append(shape.text)
    return '\n'.join(text_runs)

def extract_text_from_docx(file_path):
    doc = Document(file_path)
    full_text = []
    for para in doc.paragraphs:
        full_text.append(para.text)
    return '\n'.join(full_text)

def extract_text_from_odt(file_path):
    # ODT files are essentially XML files in a zip archive
    text_content = []
    with zipfile.ZipFile(file_path, 'r') as zip_ref:
        for file in zip_ref.namelist():
            if file.endswith('.xml'):
                with zip_ref.open(file) as f:
                    content = f.read().decode('utf-8')
                    soup = BeautifulSoup(content, 'xml')
                    text_content.append(soup.get_text())
    return '\n'.join(text_content)

def extract_text(file_path):
    if is_epub(file_path):
        return extract_text_from_epub(file_path)
    elif is_html(file_path):
        return extract_text_from_html(file_path)
    elif is_json(file_path):
        return extract_text_from_json(file_path)
    elif is_pptx(file_path):
        return extract_text_from_pptx(file_path)
    elif is_docx(file_path):
        return extract_text_from_docx(file_path)
    elif is_odt(file_path):
        return extract_text_from_odt(file_path)
    else:
        raise ValueError(f'Unsupported file format for {file_path}')

def save_text(text, output_file):
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(text)
    print(f'Successfully saved extracted text to {output_file}')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Script to extract text from various file formats.')
    parser.add_argument('-i', '--input', dest='input_file', help='Path to the input file', required=True)
    parser.add_argument('-o', '--output', dest='output_file', help='Path to the output text file')

    args = parser.parse_args()

    try:
        extracted_text = extract_text(args.input_file)
        if args.output_file:
            save_text(extracted_text, args.output_file)
        else:
            input_dir = os.path.dirname(os.path.abspath(args.input_file))
            base_name = os.path.splitext(os.path.basename(args.input_file))[0]
            output_file = os.path.join(input_dir, f'{base_name}_output.txt')
            save_text(extracted_text, output_file)

    except Exception as e:
        print(f'Error: {e}')
