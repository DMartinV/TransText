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
# Import necessary libraries and modules.
import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

# Execute try/except block.
try:
    # When the script is being executed as part of a package.
    from .function_imageText import extractTextFromImage, getLanguageCodes, isImageFile
except ImportError:
    # When the script is being executed as a standalone script.
    from function_imageText import extractTextFromImage, getLanguageCodes, isImageFile

def browseFile(entryImage):
    """
    This function opens a file dialog to allow users to select the input image file.
    It also updates the entry widget with the file's path.
    
    Parameters:
        * entryImage (ttk.Entry): Entry widget to update with the selected file's path.
    
    Returns:
        * None.
    """
    # Open file dialog to select the file.
    inputImageFile = filedialog.askopenfilename(title="Select Input Image File", filetypes=[("Image Files", "*.jpg *.jpeg *.png *.gif *.bmp *.tiff *.tif *.webp")])
    
    # Check if there is any text, delete it and replace it with the input file's path.
    if inputImageFile:
        entryImage.delete(0, tk.END)
        entryImage.insert(0, inputImageFile)

def saveAs(entryOutputDir, entryImage):
    """
    This function opens a file dialog for users to save the plain text file into another directory.
    It suggests a default filename based on the selected image file.
    
    Parameters:
        * entryOutputDir (ttk.Entry): Entry widget to update with the selected output file's path.
        * entryImage (ttk.Entry): Entry widget containing the source image file path.

    Returns:
        * None.
    """
    # Get the input image file path from the entry widget.
    inputImageFile = entryImage.get()
    
    # If no image file is selected, show a warning message.
    if not inputImageFile:
        messagebox.showwarning("Error", "Please select an image file.")
        return

    # Get the base name of the image file without the extension.
    baseName = os.path.splitext(os.path.basename(inputImageFile))[0]

    # Default filename based on the input image file.
    suggestedName = f"{baseName}_output.txt"

    # Open a file dialog for saving a file as plain text.
    outputPath = filedialog.asksaveasfilename(defaultextension=".txt", initialfile=suggestedName, filetypes=[("Text Files", "*.txt")])
    
    # Verify if the output path is selected.
    if outputPath:
        # Delete any existing text and insert the selected output path into the widget.
        entryOutputDir.delete(0, tk.END)
        entryOutputDir.insert(0, outputPath)

def convertFile(entryImage, comboLanguage, entryOutputDir):
    """
    This function extracts the content of the image and converts it into a plain text file.
    
    Parameters:
        * entryImage (ttk.Entry): Entry widget containing the source image file path.
        * comboLanguage (ttk.Combobox): Combobox widget containing the selected language for text extraction.
        * entryOutputDir (ttk.Entry): Entry widget containing the output file path.

    Raises:
        * FileNotFoundError: If the source file is not found.
        * Exception: If an error occurs during the conversion.

    Returns:
        * None.
    """
    # Get the source file path from the widget and the language from the combobox.
    inputImageFile = entryImage.get()
    language = comboLanguage.get()

    # Check if the input file is an image.
    if not isImageFile(inputImageFile):
        messagebox.showwarning("Error", f"The file '{inputImageFile}' is not an image.")
        return
    
    # Execute try/except block.
    try:
        # Use the "extractTextFromImage" function to extract the text from the image.
        text = extractTextFromImage(inputImageFile, language)
        
        # If extraction is successful.
        if text is not None:
            # Use the output path directly from the entry widget.
            outputPath = entryOutputDir.get()
            
            # Write the extracted text onto the output file.
            with open(outputPath, "w", encoding="utf-8") as finalFile:
                finalFile.write(text)

            # Display success message.
            messagebox.showinfo("Success", f"The conversion was a success! File: '{os.path.basename(outputPath)}' is saved in '{outputPath}'.")
            print(f"The conversion was a success! File: '{os.path.basename(outputPath)}' is saved in '{outputPath}'.")
    
    # Handle file not found error and show error message.
    except FileNotFoundError:
        messagebox.showwarning("Error", f"Source file '{inputImageFile}' not found.")

    # Handles other types of errors and show error message.
    except Exception as e:
        messagebox.showwarning("Error", f"Conversion error: {e}")

def createImageToTextGui(parent):
    """
    This function creates a GUI for extracting an image's textual content.
    
    Parameters:
        * parent (tkinter.Widget): The parent widget to create the GUI components.
    
    Returns:
        * None.
    """
    global entryImage, entryOutputDir, ComboLanguage

    # Frame that holds the components and widgets of the GUI.
    frame = ttk.Frame(parent)

    # Create and place labels, entries, and buttons.
    ttk.Label(frame, text="Image File:").grid(row=0, column=0, sticky="w", padx=10, pady=5)
    ttk.Label(frame, text="Output Directory:").grid(row=1, column=0, sticky="w", padx=10, pady=5)
    ttk.Label(frame, text="Language:").grid(row=2, column=0, sticky="w", padx=10, pady=5)

    entryImage = ttk.Entry(frame, width=40)
    entryImage.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=10, pady=5)
    entryOutputDir = ttk.Entry(frame, width=40)
    entryOutputDir.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=10, pady=5)

    ttk.Button(frame, text="Browse", command=lambda: browseFile(entryImage)).grid(row=0, column=2, padx=10, pady=5)
    ttk.Button(frame, text="Save as", command=lambda: saveAs(entryOutputDir, entryImage)).grid(row=1, column=2, padx=10, pady=5)
    ttk.Button(frame, text="Convert", command=lambda: convertFile(entryImage, ComboLanguage, entryOutputDir)).grid(row=3, column=0, columnspan=3, pady=10)

    languageCodes = getLanguageCodes()
    ComboLanguage = ttk.Combobox(frame, values=languageCodes, state="readonly", width=40)
    ComboLanguage.set("Select Language")  
    ComboLanguage.grid(row=2, column=1, padx=10, pady=5)

    # Pack the frame.
    frame.pack(fill='both', expand=True, padx=10, pady=10)

if __name__ == "__main__":
    """
    Main entry point for the app.
    Initializes the Tkinter root window (the main application).
    """
    # Initialize and set title of the root window (the main application).
    root = tk.Tk()
    root.title("Image to Text Functionality")

    # Create GUI components in the root window (the main application) and start the main event loop.
    createImageToTextGui(root)

    root.mainloop()
