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
# Import the necessary libraries and modules.
import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

# Execute try/except block.
try:
    # When the script is running as part of a package.
    from .function_fileText import extractTextFromFile, saveText
except ImportError:
    # When the script is running as a standalone script.
    from function_fileText import extractTextFromFile, saveText

def browseFile():
    """
    This function opens a file dialog for users to select a file. 
    
    Returns:
        * None
    """
    # Open a file dialog to select the file.
    inputFilePath = filedialog.askopenfilename(title="Select the Input File", filetypes=(("All Files", "*.*"),))
    
    # If file is selected, it clears any text and adds the file path into the entryInputFile entry widget.
    if inputFilePath:
        entryInputFile.delete(0, tk.END)
        entryInputFile.insert(0, inputFilePath)

def saveAs():
    """
    This function opens a file dialog for users to save the plain text file into another directory and under a different name. 
    
    Returns:
        * None
    """
    # Open a file dialog to save the output file.
    outputPath = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
    
    # If users have selected an output path, it clears any text and adds the output file's path into the entryOutputDir entry widget.
    if outputPath:
        entryOutputDir.delete(0, tk.END)
        entryOutputDir.insert(0, outputPath)

def convertFile():
    """
    This function converts the file to a plain text file.
    
    Returns:
        * None.

    Raises:
        * FileNotFoundError: If the source file is not found.
        * Exception: If an error occurs during the conversion.
    """
    # Get the entry path and the output file path from the entry widgets.    
    inputFilePath = entryInputFile.get()
    outputPath = entryOutputDir.get()

    # Execute try/except block.
    try:
        # Extract the textual content from the PDF file by calling the "extractTextFromFile" function.
        text = extractTextFromFile(inputFilePath)
        # Save the extracted text into the output file.
        saveText(text, outputPath)
        # Print a message if the conversion is a success.
        messagebox.showinfo("Success", f'The conversion was a success! File: "{os.path.basename(outputPath)}" is saved in: "{os.path.abspath(outputPath)}"')
    
    # Handle file not found error and show error message.
    except FileNotFoundError as fnfError:
        messagebox.showwarning("Error", f"Source file not found:\n{fnfError}")

    # Handle other types of errors and show error message. 
    except Exception as e:
        messagebox.showwarning("Error", f'Conversion error:\n{e}. If "{inputFilePath}" is a PDF or Excel file, try using the other features available in the program.')

def createFileToText(parent):
    """
    This function creates a GUI for extracting the text of a file and saving it onto a plain text file.

    Parameters:
        * parent (tkinter.Widget): The parent widget to create the GUI components.
    
    Returns:
        * None.
    """
    # Global variables.
    global entryInputFile, entryOutputDir
    
    # Frame that holds the components and widgets of the GUI.
    frame = ttk.Frame(parent)

    # Create and place labels, entries, and buttons.
    ttk.Label(frame, text="Source File:").grid(row=0, column=0, sticky="w", padx=10, pady=5)
    ttk.Label(frame, text="Output Directory:").grid(row=1, column=0, sticky="w", padx=10, pady=5)

    entryInputFile = ttk.Entry(frame, width=40)
    entryInputFile.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=10, pady=5)

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
    root.title("File to Text Functionality")

    # Create GUI components in the root window (the main application) and start the main event loop.
    createFileToText(root)
    root.mainloop()
