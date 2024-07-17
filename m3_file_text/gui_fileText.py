#    gui_fileText
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
This script serves as the graphical user interface of this module.
This GUI allows users to browse for file using the 'Browse' button, opening a file dialog to select the file. 
Users can also specify the output directory using the 'Save as' button.
Once users have selected their input file and saved it into the desired directory, the conversion will automatically start when the "Convert" button is clicked.
"""
# gui_fileText.py

import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import sys

try:
    # Attempt to import when the script is part of a package
    from .function_fileText import (
        extract_text_from_epub,
        extract_text_from_html,
        extract_text_from_json,
        extract_text_from_pptx,
        extract_text_from_docx,
        extract_text_from_odt,
        save_text
    )
except ImportError:
    # Fallback to importing when the script is standalone
    from function_fileText import (
        extract_text_from_epub,
        extract_text_from_html,
        extract_text_from_json,
        extract_text_from_pptx,
        extract_text_from_docx,
        extract_text_from_odt,
        save_text
    )

def browse_file():
    """
    Opens a file dialog for users to select a file of any supported type.
    """
    filetypes = [
        ("EPUB Files", "*.epub"),
        ("HTML Files", "*.html;*.htm"),
        ("JSON Files", "*.json"),
        ("PPTX Files", "*.pptx"),
        ("DOCX Files", "*.docx"),
        ("ODT Files", "*.odt"),
        ("All Files", "*.*")
    ]

    input_file = filedialog.askopenfilename(
        title="Select File",
        filetypes=filetypes
    )

    if input_file:
        entry_file.delete(0, tk.END)
        entry_file.insert(0, input_file)

def save_as():
    """
    Opens a file dialog for users to save the plain text file into another directory and under a different name.
    """
    input_file = entry_file.get()

    if not input_file:
        messagebox.showwarning("Error", "Please select a file.")
        return

    base_name = os.path.splitext(os.path.basename(input_file))[0]
    suggested_name = f"{base_name}_output.txt"

    output_path = filedialog.asksaveasfilename(
        defaultextension=".txt",
        initialfile=suggested_name,
        filetypes=[("Text Files", "*.txt")]
    )

    if output_path:
        entry_output.delete(0, tk.END)
        entry_output.insert(0, output_path)

def convert_file():
    """
    Extracts text from the selected file and saves it to the specified output file.
    """
    input_file = entry_file.get()
    output_file = entry_output.get()

    if not input_file:
        messagebox.showwarning("Error", "Please select a file.")
        return

    try:
        if input_file.endswith('.epub'):
            text = extract_text_from_epub(input_file)
        elif input_file.endswith('.html') or input_file.endswith('.htm'):
            text = extract_text_from_html(input_file)
        elif input_file.endswith('.json'):
            text = extract_text_from_json(input_file)
        elif input_file.endswith('.pptx'):
            text = extract_text_from_pptx(input_file)
        elif input_file.endswith('.docx'):
            text = extract_text_from_docx(input_file)
        elif input_file.endswith('.odt'):
            text = extract_text_from_odt(input_file)
        else:
            messagebox.showwarning("Error", "Unsupported file format.")
            return

        save_text(text, output_file)
        messagebox.showinfo("Success", f"Conversion successful! File saved as:\n{os.path.abspath(output_file)}")

    except FileNotFoundError:
        messagebox.showwarning("Error", f"File not found: {input_file}")
    except Exception as e:
        messagebox.showerror("Error", f"Conversion error: {str(e)}")

def create_gui(parent):
    """
    Creates the GUI for extracting text from various file formats and saving it into a plain text file.
    """
    global entry_file, entry_output

    frame = ttk.Frame(parent)

    ttk.Label(frame, text="File:").grid(row=0, column=0, sticky="w", padx=10, pady=5)
    ttk.Label(frame, text="Output File:").grid(row=1, column=0, sticky="w", padx=10, pady=5)

    entry_file = ttk.Entry(frame, width=40)
    entry_file.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=10, pady=5)

    entry_output = ttk.Entry(frame, width=40)
    entry_output.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=10, pady=5)

    ttk.Button(frame, text="Browse", command=browse_file).grid(row=0, column=2, padx=10, pady=5)
    ttk.Button(frame, text="Save as", command=save_as).grid(row=1, column=2, padx=10, pady=5)
    ttk.Button(frame, text="Convert", command=convert_file).grid(row=2, column=0, columnspan=3, pady=10)

    frame.pack(fill='both', expand=True, padx=10, pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("File to Text Conversion")

    create_gui(root)

    root.mainloop()
