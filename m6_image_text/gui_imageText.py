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
This script serves as the graphical user interface of this module.
This GUI allows users to browse for an image file using the 'Browse' button, opening a file dialog to select the input file. 
It also enables users to choose the language of the image from a dropdown menu and save the file output file in a different directory.
Once users have selected their input file and saved it into the desired directory, the conversion will automatically start when the "Convert" button is clicked.
"""
# Import the necessary libraries and modules.
import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

# Execute try/except block.
try:
    # When the script is being executed as part of a package.
    from function_imageText import extractTextFromImage, getLanguageCodes
except ImportError:
    # When the script is being executed as a standalone script.
    from .function_imageText import extractTextFromImage, getLanguageCodes

def browseFile():
    """
    This function opens a file dialog to allow users to select the input image file.
    It also updates the entry widget with the file's path.
    
    Returns:
        * None.
    """
    # Open file dialog to select the file.
    filePath = filedialog.askopenfilename(title="Select Input Image File", filetypes=[("Image Files", "*.jpg *.jpeg *.png *.gif *.bmp *.tiff *.tif *.webp")])
    
    # Check if there is any text, delete it and replace it with the input file's path.
    if filePath:
        entrySource.delete(0, tk.END)
        entrySource.insert(0, filePath)
        
        # If the output file name entry widget is empty, generate a default file name based on the input image file name.
        if not entryOutputName.get():
            # Generate default name based on the input image file.
            baseName = os.path.splitext(os.path.basename(filePath))[0]
            # Insert the default name into the entry widget.
            entryOutputName.insert(0, baseName)

def saveAs():
    """
    This function opens a file dialog for users to save the plain text file into another directory.
    It suggests a default filename based on the selected image file.
    
    Returns:
        * None.
    """
    # Get the base name from the source image file path.
    inputFileName = os.path.splitext(os.path.basename(entrySource.get()))[0]
    
    # Open a file dialog to save the file.
    directoryPath = filedialog.asksaveasfilename(initialfile=inputFileName, defaultextension=".txt", filetypes=(("Plain Text", "*.txt"), ("All Files", "*.*")))
    # If the user chooses a directory path. 
    if directoryPath:
        # Clear the output directory entry widget and insert the chosen directory path.
        entryOutputDir.delete(0, tk.END)
        outputDir, outputFile = os.path.split(directoryPath)
        entryOutputDir.insert(0, outputDir)
        # Clear the output file name entry widget and insert the file name.
        entryOutputName.delete(0, tk.END)
        entryOutputName.insert(0, outputFile)

def convertFile():
    """
    This function extracts the content of the image and converts it into a plain text file.

    Returns:
        * None.
    """
    # Get the source file path from the widget and the language from the combobox.
    sourcePath = entrySource.get()
    language = ComboLanguage.get()

    # Use the "extractTextFromImage" function to extract the text from the image.
    text = extractTextFromImage(sourcePath, language)

    # If extraction is successful.
    if text is not None:
        # Use the output path directly from the entry widget.
        outputDirectory = entryOutputDir.get()
        outputFileName = entryOutputName.get()

        if not outputFileName:
            # If the user has not provided an output file name, show a warning message.
            messagebox.showwarning("Error", "Please provide a file name.")
            return
        
        # Construct the full output file path.
        outputFilePath = os.path.join(outputDirectory, outputFileName)
        
        # Write the extracted text onto the output file.
        with open(outputFilePath, "w", encoding="utf-8") as outputFile:
            outputFile.write(text)
        
        # Show an the success message.
        messagebox.showinfo("Success", f"The text has been extracted and saved to: {outputFilePath}")

def createImageToTextGui(parent):
    """
    This function creates a GUI for extracting an image's textual content.
    
    Parameters:
        * parent (tkinter.Widget): The parent widget to create the GUI components.
    
    Returns:
        * None.
    """
    global entrySource, entryOutputDir, entryOutputName, ComboLanguage

    # Frame that holds the components and widgets of the GUI.
    frame = ttk.Frame(parent)
    
    # Create and place labels, entries, and buttons.
    labelSource = ttk.Label(frame, text="Image File:")
    labelSource.grid(row=0, column=0, sticky="w", padx=10, pady=5)  

    labelOutputDir = ttk.Label(frame, text="Output Directory:")
    labelOutputDir.grid(row=1, column=0, sticky="w", padx=10, pady=5)  

    labelOutputName = ttk.Label(frame, text="Output File Name:")
    labelOutputName.grid(row=2, column=0, sticky="w", padx=10, pady=5)  

    labelLanguage = ttk.Label(frame, text="Language:")
    labelLanguage.grid(row=3, column=0, sticky="w", padx=10, pady=5)  

    entrySource = ttk.Entry(frame, width=40)
    entrySource.grid(row=0, column=1, sticky="we", padx=10, pady=5) 

    entryOutputDir = ttk.Entry(frame, width=40)
    entryOutputDir.grid(row=1, column=1, sticky="we", padx=10, pady=5) 

    entryOutputName = ttk.Entry(frame, width=40)
    entryOutputName.grid(row=2, column=1, sticky="we", padx=10, pady=5) 

    buttonBrowse = ttk.Button(frame, text="Browse", command=browseFile)
    buttonBrowse.grid(row=0, column=2, padx=10, pady=5) 

    buttonSaveAs = ttk.Button(frame, text="Save as", command=saveAs)
    buttonSaveAs.grid(row=1, column=2, padx=10, pady=5) 

    buttonConvert = ttk.Button(frame, text="Convert", command=convertFile)
    buttonConvert.grid(row=4, column=0, columnspan=3, pady=10)  

    languageCodes = getLanguageCodes()
    ComboLanguage = ttk.Combobox(frame, values=languageCodes, width=37)
    ComboLanguage.grid(row=3, column=1, sticky="we", padx=10, pady=5) 
    ComboLanguage.set("Select Language")
    
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
