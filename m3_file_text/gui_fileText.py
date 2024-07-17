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
# Import necessary libraries and modules.
import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

try:
    # Try to import when the script is being run as part of a package.
    from .function_fileText import (
        extractTextFromEpub,
        extractTextFromHtml,
        extractTextFromJson,
        extractTextFromPptx,
        extractTextFromDocx,
        saveText
    )
except ImportError:
    # Try importing when the script is being run as a standalone file.
    from function_fileText import (
        extractTextFromEpub,
        extractTextFromHtml,
        extractTextFromJson,
        extractTextFromPptx,
        extractTextFromDocx,
        saveText
    )

def browseFile():
    """
    This function opens a file dialog for the user to select a file. 
    
    Returns:
        * None
    """
    # File types options.
    fileTypes = [
        ("EPUB Files", "*.epub"),
        ("HTML Files", "*.html;*.htm"),
        ("JSON Files", "*.json"),
        ("PPTX Files", "*.pptx"),
        ("DOCX Files", "*.docx"),
        ("All Files", "*.*")
    ]
    # Open a file dialog to select the file.
    inputFile = filedialog.askopenfilename(title="Select the Input File",filetypes=fileTypes)
    
    # If file is selected, it clears any text and adds the file path.
    if inputFile:
        entryFile.delete(0, tk.END)
        entryFile.insert(0, inputFile)

def saveAs():
    """
    This function opens a file dialog for the user to save the plain text file into another directory. 
    
    Returns:
        * None
    """
    # Get the input file path from the entry widget.
    inputFile = entryFile.get()
    
    # If the user has not selected an input file, show error message.
    if not inputFile:
        messagebox.showwarning("Error", "Please select a file.")
        return
    
    # Get the base name of the file without the extension.
    baseName = os.path.splitext(os.path.basename(inputFile))[0]
    # Default output filename based on the input file.
    suggestedName = f"{baseName}_output.txt"

    # Open a file dialog to save the output file.
    outputPath = filedialog.asksaveasfilename(defaultextension=".txt",initialfile=suggestedName,filetypes=[("Text Files", "*.txt")])

    # If the user has selected an output path, it clears any text and adds the output file's path.
    if outputPath:
        entryOutput.delete(0, tk.END)
        entryOutput.insert(0, outputPath)

def convertFile():
    """
    This function converts the file to a plain text file.
    
    Returns:
        * None.

    Raises:
        * FileNotFoundError: If the source file is not found.
        * Exception: If an error occurs during the conversion.
    """
    # Get the entry path and the output file path.
    inputFile = entryFile.get()
    outputFile = entryOutput.get()
    
    # If the user has not selected an input file, show error message.
    if not inputFile:
        messagebox.showwarning("Error", "Please select a file.")
        return
    
    # Execute try/except block
    try:
        # Verify the file extension and call the corresponding extraction function.
        if inputFile.endswith('.epub'):
            text = extractTextFromEpub(inputFile)
        elif inputFile.endswith('.html') or inputFile.endswith('.htm'):
            text = extractTextFromHtml(inputFile)
        elif inputFile.endswith('.json'):
            text = extractTextFromJson(inputFile)
        elif inputFile.endswith('.pptx'):
            text = extractTextFromPptx(inputFile)
        elif inputFile.endswith('.docx'):
            text = extractTextFromDocx(inputFile)
        else:
            # Show warning message if the file is not supported in this program.
            messagebox.showwarning("Error", "Unsupported file format.")
            return
        # Call the function to save text.
        saveText(text, outputFile)
        # Show information message.
        messagebox.showinfo("Success", f'The conversion was a success. File: "{os.path.basename(outputFile)}" is saved in: "{os.path.abspath(outputFile)}"')
    # Handle file not found error and display error message.
    except FileNotFoundError:
        messagebox.showwarning("Error", f"File not found: {inputFile}")
    # Handle other types of errors and display error message. 
    except Exception as e:
        messagebox.showerror("Error", f"Conversion error: {str(e)}")

def createFileToText(parent):
    """
    This function creates a GUI for extracting the text of a file and saving it onto a plain text file.

    Parameters:
        * parent (tkinter.Widget): The parent widget to create the GUI components.
    
    Returns:
        * None.
    """
    global entryFile, entryOutput
    
    # Frame to hold the components and widgets of the GUI.
    frame = ttk.Frame(parent)

    # Create and place labels, entries, and buttons.
    ttk.Label(frame, text="File:").grid(row=0, column=0, sticky="w", padx=10, pady=5)
    ttk.Label(frame, text="Output File:").grid(row=1, column=0, sticky="w", padx=10, pady=5)

    entryFile = ttk.Entry(frame, width=40)
    entryFile.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=10, pady=5)

    entryOutput = ttk.Entry(frame, width=40)
    entryOutput.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=10, pady=5)

    ttk.Button(frame, text="Browse", command=browseFile).grid(row=0, column=2, padx=10, pady=5)
    ttk.Button(frame, text="Save as", command=saveAs).grid(row=1, column=2, padx=10, pady=5)
    ttk.Button(frame, text="Convert", command=convertFile).grid(row=2, column=0, columnspan=3, pady=10)

    # Pack the frame into the main application.
    frame.pack(fill='both', expand=True, padx=10, pady=10)

if __name__ == "__main__":
    """
    Main entry point for the app.
    Initializes the Tkinter root window (the main application).
    """
    # Initialize and set title of the root window (the main application).
    root = tk.Tk()
    root.title("File to Text Functionality")
    
    # Create GUI components in the root window (the main application) and start the main event loop.
    createFileToText(root)
    root.mainloop()
