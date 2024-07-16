#    gui_convertEncoding
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
This GUI allows users to browse for a file using the 'Browse' button, which opens a file dialog to select the input file. 
It also enables users to choose the desired encoding from a dropdown menu and save the output file in a different directory.
Once users have selected their input file and saved it into the desired directory, the conversion will automatically start when the "Convert" button is clicked.
"""

# Import necessary libraries and modules.
import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

# Execute try/except block.
try:
    # When the script is running as part of a package.
    from .function_convertEncoding import detectEncoding, convertEncoding
except ImportError:
    # When the script is running as a standalone script.
    from function_convertEncoding import detectEncoding, convertEncoding

# Encoding list without the ''.
from encodings import aliases

# Create a list of encodings aliases and remove apostrophes.
encoding_list = [encoding.replace("'", "") for encoding in aliases.aliases.keys()]

def browseFile(entryInputFile):
    """
    This function opens a file dialog in order to allow users to select the entry file. It also updates the entry widget with the file's path.

    Parameters:
        * entry (str): Path of the entry file.

    Returns:
        * None.
    """
    # Open file dialog to select the file.
    inputFilePath = filedialog.askopenfilename(title="Select the input File", filetypes=(("All Files", "*.*"),))

    # If the entry has any sort text, it deletes the content and adds the path of the select file.
    if inputFilePath:
        entryInputFile.delete(0, tk.END)
        entryInputFile.insert(0, inputFilePath)

def getEncodings():
    """
    This function returns a list of encodings.
    
    Returns:
        * list: sorted list of encodings.
    """
    # Return the sorted list of encodings.
    return sorted(encoding_list)

def updateEncoding(event, combo):
    """
    This function prints the list of sorted encodings into the combobox widget.

    Parameters:
        * combo (ttk.Combobox): The combobox widget from which users can select the available encodings.
    
    Returns:
        * None.
    """
    # Obtain the selected encoding from the combobox widget.
    selection = combo.get()

def convertFile(entryInputFile, combo, entryOutputDir):
    """
    This function converts the file into a specified character encoding.

    Parameters:
        * entryInputFile (ttk.Entry): Entry widget that contains the path of the entry file. 
        * combo (ttk.Combobox): Combobox widget that contains a list of the available encodings. 
        * entryOutputDir (ttk.Entry): Entry widget that constains the path where the output file will be saved.
    
    Returns:
        * None.
    
    Raises:
        * FileNotFoundError: If the source file is not found.
        * Exception: If an error occurs during the conversion.
    """
    # Retrieve the entry path and the desired encoding.
    sourcePath = entryInputFile.get()
    outputEncoding = combo.get()

    # Execute try/except block
    try:
        # Check if the source and the output encoding are the same.
        sourceEncoding = detectEncoding(sourcePath)
        
        # If the source and the output encoding are the same, no conversion is needed.
        if sourceEncoding == outputEncoding:
            messagebox.showinfo("No Conversion Needed", "The input file and output file have the same encoding. No conversion needed.")
        
        # If it is not the same, execute conversion.
        else:
            # Get output directory path.
            outputDirectory = entryOutputDir.get()
            
            # If the output directory is not specified, it uses the same directory as in the source file.
            if not outputDirectory:
                outputDirectory = os.path.dirname(sourcePath)

            # Extract the base name and the extension of the source file.
            baseName, extension = os.path.splitext(os.path.basename(sourcePath))
            newName = entryOutputDir.get() 
            
            # Check whether the name of the output file is determined by users or the default.
            if newName:
                outputPath = os.path.join(outputDirectory, f"{newName}{extension}")
            else:
                outputPath = os.path.join(outputDirectory, f"{baseName}_{outputEncoding}{extension}")

            # Convert the file's encoding.
            convertEncoding(sourcePath, outputEncoding, outputPath)

            # Display success message when the conversion has been successful.
            messagebox.showinfo("Success", f"The conversion was a success. File: '{os.path.basename(outputPath)}' is saved in '{outputPath}'.")    
    # Handle file not found error and display warning message.
    except FileNotFoundError:
        messagebox.showwarning("Error", f'Source file: "{sourcePath}" not found.')

    # Handle other types of errors and display warning message.
    except Exception as e:
        messagebox.showwarning("Error", f'Conversion error: {e}')

def saveAs(entryOutputDir, entryInputFile):
    """
    This function opens a file dialog to select the directory where users are going to save the output file.

    Parameters:
        * entryOutputDir (ttk.Entry): Entry widget that contains the path where the output file will be saved.
        * entryInputFile (ttk.Entry): Entry widget that contains the path of the input file.

    Returns:
        * None
    """
    # Get the input file path from the entry widget.
    inputFilePath = entryInputFile.get()
    
    # If no file is imported into the program, show a warning message.
    if not inputFilePath:
        messagebox.showwarning("Error", "Please select a file.")
        return

    # Get the base name of the input file without the extension.
    baseName, _ = os.path.splitext(os.path.basename(inputFilePath))
    
    # Default output filename based on the input file.
    suggestedName = f"{baseName}_output"

    # Open a file dialog to save the output file.
    outputPath = filedialog.asksaveasfilename(initialfile=suggestedName, filetypes=[("Text Files", "*.txt")])

    # If users have selected an output path, it clears any text and adds the path into the entry widget.
    if outputPath:
        entryOutputDir.delete(0, tk.END)
        entryOutputDir.insert(0, outputPath)


def createConvertEncodingGui(parent):
    """
    This function creates a GUI for selecting and converting a file's encoding.

    Parameters:
        * parent (tkinter.Widget): The parent widget to create the GUI components.
    
    Returns:
        * None.
    """
    # Frame that holds the components and widgets of the GUI.
    frame = ttk.Frame(parent)

    # Create and place labels, entries and buttons.
    ttk.Label(frame, text="Source File:").grid(row=0, column=0, sticky="w", padx=10, pady=5)
    ttk.Label(frame, text="Output Encoding:").grid(row=1, column=0, sticky="w", padx=10, pady=5)
    ttk.Label(frame, text="Output Directory:").grid(row=2, column=0, sticky="w", padx=10, pady=5)

    entryInputFile = ttk.Entry(frame, width=40)
    entryInputFile.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=10, pady=5)
    entryOutputDir = ttk.Entry(frame, width=40)
    entryOutputDir.grid(row=2, column=1, sticky=(tk.W, tk.E), padx=10, pady=5)

    ttk.Button(frame, text="Browse", command=lambda: browseFile(entryInputFile)).grid(row=0, column=2, padx=10, pady=5)
    ttk.Button(frame, text="Save as", command=lambda: saveAs(entryOutputDir, entryInputFile)).grid(row=2, column=2, padx=10, pady=5)
    ttk.Button(frame, text="Convert", command=lambda: convertFile(entryInputFile, combo, entryOutputDir)).grid(row=4, column=0, columnspan=3, pady=10)

    encodings = getEncodings()
    combo = ttk.Combobox(frame, values=encoding_list, state="readonly", width=40)
    combo.set("Select encoding")  
    combo.grid(row=1, column=1, padx=10, pady=5)

    combo.bind("<<ComboboxSelected>>", lambda event: updateEncoding(event, combo))
    
    # Pack the frame.
    frame.pack(fill='both', expand=True, padx=10, pady=10)

if __name__ == "__main__":
    """
    Main entry point for the app.
    It initializes the Tkinter root window (the main application).
    """
    # Initialize and set title of the root window (the main application).
    root = tk.Tk()
    root.title("Convert Encoding Functionality")

    # Create GUI components in the root window (the main application) and start the main event loop.
    createConvertEncodingGui(root)

    root.mainloop()
