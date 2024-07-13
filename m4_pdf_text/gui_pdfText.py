#    gui_pdfText
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
This GUI allows users to browse for a PDF file using the 'Browse' button, opening a file dialog to select the PDF file. 
Users can also specify the output directory using the 'Save as' button.
Once users have selected their input file and saved it into the desired directory, the conversion will automatically start when the "Convert" button is clicked.
"""

# Import the necessary libraries and modules.
import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

# Execute try/except block.
try:
    # When the script is being executed as part of a package.
    from .function_pdfText import extractTextFromPdf, saveText
except ImportError:
    # When the script is being executed as a standalone script.
    from function_pdfText import extractTextFromPdf, saveText


def browseFile():
    """
    This function opens a file dialog for users to select a PDF file. 
    
    Returns:
        * None.
    """
    # Open a file dialog to select the PDF file.
    inputPdfFile = filedialog.askopenfilename(title="Select PDF File", filetypes=[("PDF Files", "*.pdf")])
    
    # If the file is a PDF, it clears any text and adds the PDF path into the entryPdf entry widget.
    if inputPdfFile:
        entryPdf.delete(0, tk.END)
        entryPdf.insert(0, inputPdfFile)

def saveAs():
    """
    This function opens a file dialog for users to save the plain text file into another directory and under a different name. 
    
    Returns:
        * None.
    """
    # Open a file dialog to save the output file.
    outputPath = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
    
    # If users have selected an output path, it clears any text and adds the output file's path in the entryOutputDir entry widget.
    if outputPath:
        entryOutputDir.delete(0, tk.END)
        entryOutputDir.insert(0, outputPath)

def convertFile():
    """
    This function converts the extracted text into a plain text file.
    
    Returns:
        * None.

    Raises:
        * FileNotFoundError: If the source file is not found.
        * Exception: If an error occurs during the conversion.

    """
    
    # Get the paths from the input and output files from the entry widgets.
    inputPdfFile = entryPdf.get()
    outputPath = entryOutputDir.get()

    # Execute try/except block.
    try:
        # Extract the textual content from the PDF file, using the "extractTextFromPdf".
        text = extractTextFromPdf(inputPdfFile)
        # Save the extracted text to the output file.
        saveText(text, outputPath)
        # Print success message.
        messagebox.showinfo("Success", f'The conversion was a success! File: "{os.path.basename(outputPath)}" is saved in: "{os.path.abspath(outputPath)}"')
    
    # Handle file not found error and show error message.
    except FileNotFoundError:
        messagebox.showwarning("Error", f'Source file: "{inputPdfFile}" not found.')

    # Handle other types of errors and display error message. 
    except Exception as e:
        messagebox.showwarning("Error", f'Conversion error: {e}')

def createPdfToTextGui(parent):
    """
    This function creates a GUI for extracting the text of a PDF and saving it into a plain text file.

    Args:
        * parent (tkinter.Widget): The parent widget to create the GUI components.
    
    Returns:
        * None.
    """
    # Global variables.
    global entryPdf, entryOutputDir

    # Frame that holds the components and widgets of the GUI.
    frame = ttk.Frame(parent)

    # Create and place labels, entries, and buttons.
    ttk.Label(frame, text="PDF File:").grid(row=0, column=0, sticky="w", padx=10, pady=5)
    ttk.Label(frame, text="Output Directory:").grid(row=1, column=0, sticky="w", padx=10, pady=5)

    entryPdf = ttk.Entry(frame, width=40)
    entryPdf.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=10, pady=5)
    entryOutputDir = ttk.Entry(frame, width=40)
    entryOutputDir.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=10, pady=5)

    ttk.Button(frame, text="Browse", command=browseFile).grid(row=0, column=2, padx=10, pady=5)
    ttk.Button(frame, text="Save as", command=saveAs).grid(row=1, column=2, padx=10, pady=5)
    ttk.Button(frame, text="Convert", command=convertFile).grid(row=2, column=0, columnspan=3, pady=10)

    # Pack the frame.
    frame.pack(fill='both', expand=True, padx=10, pady=10)

if __name__ == "__main__":
    """
    Main entry point for the app.
    Initialize the Tkinter root window (the main application).

    """
    # Initialize and set title of the root window (the main application).
    root = tk.Tk()
    root.title("PDF to Text Functionality")
    
    # Create GUI components in the root window (the main application) and start the main event loop.
    createPdfToTextGui(root)
    root.mainloop()