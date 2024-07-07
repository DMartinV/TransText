#    gui_detectEncoding
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
This GUI allows users to browse for a file using the 'Browse' button, which opens a file dialog to select the input file. After selecting the file, users must click the 'Detect' button to automatically display the file's encoding.
"""

#Imports necessary libraries.
import tkinter as tk
from tkinter import ttk, filedialog

# Executes try/except block.
try:
    # When running as part of a package.
    from .function_detectEncoding import detectEncoding
except ImportError:
    # When running as a standalone script.
    from function_detectEncoding import detectEncoding

def browseFile(entryInputFile):
    """
    This function opens a file dialog in order to allow users to select an input file. It also updates the entry widget with the file's path.

    Args:
        * entryInputFile (tkinter.Entry): The entry widget that contains the input file's path.

    Returns:
        * None.
    """
    # Opens file dialog to select the file.
    inputFilePath = filedialog.askopenfilename(title="Select the input File")
    
    # If it has any text, it deletes the content and adds the path of the select file.
    if inputFilePath:
        entryInputFile.delete(0, tk.END)
        entryInputFile.insert(0, inputFilePath)

def detectEncoding(entryInputFile, entryEncoding):
    """
    This function detects the file's encoding and displays the result in the entryEncoding entry widget.

    Args:
        * entryInputFile (tkinter.Entry): Entry widget that has the entry file's path.
        * entryEncoding (tkinter.Entry): Entry widget that displays the encoding of the entry file.

    Returns:
        * None.
    """

    # Gets the file's path from the entryInputFile widget.
    entryInputFile_text = entryInputFile.get()

    # Detects the encoding of the file using the function script.
    encoding = detectEncoding(entryInputFile_text)

    # Deletes any text from the entryEncoding widget.
    entryEncoding.delete(0, tk.END)

    # Adds the encoding into the entryEncoding widget.
    entryEncoding.insert(0, encoding)

def createDetectEncodingGui(parent):
    """
    This function creates a GUI for selecting and displaying a file's encoding.

    Args:
        * parent (tkinter.Widget): Parent widget to create the GUI components.
    
    Returns:
        None.
    """
    # Frame to hold the components and widgets of the gui.
    frame = ttk.Frame(parent)

    # Creates and place labels, entries and buttons.
    ttk.Label(frame, text="Source File:").grid(row=0, column=0, sticky="w", padx=10, pady=5)
    ttk.Label(frame, text="Detected Encoding:").grid(row=1, column=0, sticky="w", padx=10, pady=5)

    entryInputFile = ttk.Entry(frame, width=40)
    entryInputFile.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=10, pady=5)
    entryEncoding = ttk.Entry(frame, width=40)
    entryEncoding.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=10, pady=5)

    ttk.Button(frame, text="Browse", command=lambda: browseFile(entryInputFile)).grid(row=0, column=2, padx=10, pady=5)
    ttk.Button(frame, text="Detect", command=lambda: detectEncoding(entryInputFile, entryEncoding)).grid(row=1, column=2, padx=10, pady=5)

    # Packs the frame into the main application.
    frame.pack(fill='both', expand=True, padx=10, pady=10)

if __name__ == "__main__":
    """
    Main entry point for the app.
    Initializes the Tkinter root window (the main application).
    """
    # Initializes and sets title of the root window (the main application).
    root = tk.Tk()
    root.title("Detect Encoding Functionality")

    # Creates GUI components in the root window (the main application) and starts the main event loop.
    createDetectEncodingGui(root)
    root.mainloop()
