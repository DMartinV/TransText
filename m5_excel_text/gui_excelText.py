#    gui_excelText
#    Copyright (C) 2024  Diana Martin Vilá
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
This GUI allows users to browse for an Excel file using the 'Browse' button, which opens a file dialog to select the file. 
Users can also specify the output directory using the 'Save as' button.
Once users have selected their input file and saved it into the desired directory, the conversion will automatically start when the "Convert" button is clicked.
"""
# Import necessary libraries and modules.
import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

# Execute try/except block.
try:
    # When the script is running as part of a package.
    from .function_excelText import extractTextFromExcel, saveText
except ImportError:
    # When the script is running as a standalone script.
    from function_excelText import extractTextFromExcel, saveText

def browseFile():
    """
    This function opens a file dialog for users to select an Excel file. 
    
    Returns:
        * None.
    """
    # Open a file dialog to select the Excel file.
    inputExcelFile = filedialog.askopenfilename(filetypes=[("Excel files", "*.xls *.xlsx *.xlsm *.xlsb *.odf *.ods")])
    
    # If the file is an Excel file, it clears any text and adds the input Excep path into the entryExcel entry widget.
    if inputExcelFile:
        entryExcel.delete(0, tk.END)
        entryExcel.insert(0, inputExcelFile)

def saveAs():
    """
    This function opens a file dialog for users to save the plain text file into another directory. 
    
    Returns:
        * None.
    """
    # Open a file dialog to save the output file.
    outputPath = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
    
    # If users have selected an output path, it clears any text and adds the output file's path into the entryOutputDir entry widget.
    if outputPath:
        entryOutputDir.delete(0, tk.END)
        entryOutputDir.insert(0, outputPath)

def convertFile():
    """
    This function extracts text from the selected Excel file and saves it to a text file.
    
    Returns:
        * None.
    """
    # Get the path of the Excel file and the output directory from the entry widgets.
    inputExcelFile = entryExcel.get()
    outputPath = entryOutputDir.get()

    # Execute try/except block.
    try:
        # Extract the textual content from the Excel file by calling the "extractTextFromExcel" function.
        text = extractTextFromExcel(inputExcelFile)
        
        # Save the extracted text to the output file.
        saveText(text, outputPath)
        
        # Display sucess message.
        messagebox.showinfo("Success", f'The conversion was a success! File: "{os.path.basename(outputPath)}" is saved in: "{os.path.abspath(outputPath)}"')
    
    # Handle file not found error and show an error message.
    except FileNotFoundError:
        messagebox.showwarning("Error", f'Source file: "{inputExcelFile}" not found.')

    # Handle other types of errors and show an error message. 
    except Exception as e:
        messagebox.showwarning("Error", f'Conversion error: {e}')

def createExcelToTextGui(parent):
    """
    This function creates a GUI for extracting an Excel's textual content.
    
    Parameters:
        * parent (tkinter.Widget): The parent widget to create the GUI components.
    
    Returns:
        * None.
    """
    global entryExcel, entryOutputDir
    
    excelPath = tk.StringVar()
    outputFile = tk.StringVar()

    # Frame that holds the components and widgets of the GUI.
    frame = ttk.Frame(parent)

    # Create and place labels, entries, and buttons.
    ttk.Label(frame, text="Excel File:").grid(row=0, column=0, sticky="w", padx=10, pady=5)
    ttk.Label(frame, text="Output Directory:").grid(row=1, column=0, sticky="w", padx=10, pady=5)

    entryExcel = ttk.Entry(frame, textvariable=excelPath, width=40)
    entryExcel.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=10, pady=5)
    entryOutputDir = ttk.Entry(frame, textvariable=outputFile, width=40)
    entryOutputDir.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=10, pady=5)

    ttk.Button(frame, text="Browse", command=browseFile).grid(row=0, column=2, padx=10, pady=5)
    ttk.Button(frame, text="Save as", command=saveAs).grid(row=1, column=2, padx=10, pady=5)
    ttk.Button(frame, text="Convert", command=convertFile).grid(row=2, column=0, columnspan=3, pady=10)

    # Pack the frame.
    frame.pack(fill='both', expand=True, padx=10, pady=10)

if __name__ == "__main__":
    """
    Main entry point for the app.
    Initializes the Tkinter root window (the main application).
    """
    # Initialize and set title of the root window (the main application).
    root = tk.Tk()
    root.title("Excel to Text Functionality")

    # Create GUI components in the root window (the main application) and start the main event loop.
    createExcelToTextGui(root)

    root.mainloop()