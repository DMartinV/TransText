#    gui_imageText
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
This GUI allows users to browse for an image file using the 'Browse' button, opening a file dialog to select the input file. 
It also enables users to choose the language of the image from a dropdown menu and save the file output file in a different directory.
Once users have selected their input file and saved it into the desired directory, the conversion will automatically start when the "Convert" button is clicked.
"""
#Imports necessary libraries.
import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

# Executes try/except block.
try:
    # When running as part of a package.
    from .function_imageText import extractTextFromImage, getLanguageCodes
except ImportError:
    # When running as a standalone script.
    from function_imageText import extractTextFromImage, getLanguageCodes

def browseFile(entryImage):
    """
    This function opens a file dialog to allow the user to select the entry file.
    It also updates the entry widget with the file's path.
    
    Args:
        * entryImage (ttk.Entry): Entry widget to update with the selected file's path.
    
    Returns:
        * None.
    """
    # Opens file dialog to select the file.
    inputImageFile = filedialog.askopenfilename()
    
    # Checks if there is any text, deletes it and replaces it with the input file's path.
    if inputImageFile:
        entryImage.delete(0, tk.END)
        entryImage.insert(0, inputImageFile)

def saveAs(entryOutputDir):
    """
    This function opens a file dialog for the user to save the plain text file into another directory.

    Args:
        * entryOutputDir (ttk.Entry): Entry widget to update with the selected output file's path.

    Returns:
        * None.
    """
    # Open a file dialog for saving a file as plain text
    outputPath = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
    
    # Verifies if the output path is selected
    if outputPath:
        # Deletes any existing text and inserts the selected output path into the widget
        entryOutputDir.delete(0, tk.END)
        entryOutputDir.insert(0, outputPath)

def convertFile(entryImage, comboLanguage, entryOutputDir):
    """
    This function extracts the content of the image and converts it into a plain text file.
    
    Args:
        * entryImage (ttk.Entry): Entry widget containing the source image file path.
        * comboLanguage (ttk.Combobox): Combobox widget containing the selected language for text extraction.
        * entryOutputDir (ttk.Entry): Entry widget containing the output file path.

    Raises:
        * FileNotFoundError: If the source file is not found.
        * Exception: If an error occurs during the conversion.

    Returns:
        * None.
    """
    # Executes try/except block.
    try:
        # Gets the source file path from the widget and the language from the combobox.
        inputImageFile = entryImage.get()
        language = comboLanguage.get()

        # Uses the 'extractTextFromImage' function to extract the text from the image.
        text = extractTextFromImage(inputImageFile, language)
        
        # If extraction is successful.
        if text is not None:
            # Uses the output path directly from the entry widget.
            outputPath = entryOutputDir.get()
            
            # Writes the extracted text onto the output file.
            with open(outputPath, "w", encoding="utf-8") as finalFile:
                finalFile.write(text)

            # Display success message.
            messagebox.showinfo("Success", f"The conversion was a success. File: '{os.path.basename(outputPath)}' is saved in '{outputPath}'.")
    
    # Handles file not found error.
    except FileNotFoundError:
        messagebox.showwarning("Error", f"Source file '{inputImageFile}' not found.")

    # Handles other types of errors.
    except Exception as e:
        messagebox.showwarning("Error", f"Conversion error: {e}")

def createImageToTextGui(parent):
    """
    This function creates a GUI for extracting an image's textual content.
    
    Args:
        * parent (tkinter.Widget): The parent widget to create the GUI components.
    
    Returns:
        * None.
    """
    global entrySource, entryOutputDir, ComboLanguage

    # Frame to hold the components and widgets of the GUI.
    frame = ttk.Frame(parent)

    # Creates and place labels, entries, and buttons.
    ttk.Label(frame, text="Image File:").grid(row=0, column=0, sticky="w", padx=10, pady=5)
    ttk.Label(frame, text="Output Directory:").grid(row=1, column=0, sticky="w", padx=10, pady=5)
    ttk.Label(frame, text="Language:").grid(row=2, column=0, sticky="w", padx=10, pady=5)

    entrySource = ttk.Entry(frame, width=40)
    entrySource.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=10, pady=5)
    entryOutputDir = ttk.Entry(frame, width=40)
    entryOutputDir.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=10, pady=5)

    ttk.Button(frame, text="Browse", command=lambda: browseFile(entrySource)).grid(row=0, column=2, padx=10, pady=5)
    ttk.Button(frame, text="Save as", command=lambda: saveAs(entryOutputDir)).grid(row=1, column=2, padx=10, pady=5)
    ttk.Button(frame, text="Convert", command=lambda: convertFile(entrySource, ComboLanguage, entryOutputDir)).grid(row=3, column=0, columnspan=3, pady=10)

    languageCodes = getLanguageCodes()
    ComboLanguage = ttk.Combobox(frame, values=languageCodes, state="readonly", width=40)
    ComboLanguage.set("Select Language")  
    ComboLanguage.grid(row=2, column=1, padx=10, pady=5)

    # Packs the frame into the main application.
    frame.pack(fill='both', expand=True, padx=10, pady=10)

if __name__ == "__main__":
    """
    Main entry point for the app.
    Initializes the Tkinter root window (the main application).
    """
    # Initializes and sets title of the root window (the main application).
    root = tk.Tk()
    root.title("Image to Text Functionality")

    # Creates GUI components in the root window (the main application) and starts the main event loop.
    createImageToTextGui(root)

    root.mainloop()
