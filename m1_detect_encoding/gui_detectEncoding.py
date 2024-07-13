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

# Import necessary libraries and modules.
import tkinter as tk
from tkinter import ttk, filedialog

# Execute try/except block.
try:
    # When script is running as part of a package.
    from .function_detectEncoding import detectEncoding
except ImportError:
    # When script is running as a standalone script.
    from function_detectEncoding import detectEncoding

def browseFile(entryInputFile):
    """
    This function opens a file dialog in order to allow users to select an input file.
    It also updates the entry widget with the file's path.

    Parameters:
        * entryInputFile (tkinter.Entry): The entry widget that contains the input file's path.

    Returns:
        * None.
    """
    # Open file dialog to select the file.
    inputFilePath = filedialog.askopenfilename(title="Select the Input File", filetypes=(("All Files", "*.*"),))
    
    # If the entry has any sort text, it deletes the content and adds the path of the select file.
    if inputFilePath:
        entryInputFile.delete(0, tk.END)
        entryInputFile.insert(0, inputFilePath)

def displayEncoding(entryInputFile, entryEncoding):
    """
    This function detects the file's encoding and displays the result in an entry widget.

    Parameters:
        * entryInputFile (tkinter.Entry): Entry widget that has the path of the entry file.
        * entryEncoding (tkinter.Entry): Entry widget that displays the encoding of the entry file.

    Returns:
        * None.
    """
    # Get the file's path from the entryInputFile widget.
    entryInputFile_text = entryInputFile.get()

    # Detect the encoding of the file using the functional script.
    encoding = detectEncoding(entryInputFile_text)

    # Delete any text from the entryEncoding widget.
    entryEncoding.delete(0, tk.END)

    # Add the encoding into the entryEncoding widget.
    entryEncoding.insert(0, encoding)

def createDetectEncodingGui(parent):
    """
    This function creates a GUI for selecting and displaying a file's encoding.

    Parameters:
        * parent (tkinter.Widget): Parent widget to create the GUI components.
    
    Returns:
        None.
    """
    # Frame that holds the components and widgets of the GUI.
    frame = ttk.Frame(parent)

    # Create and place labels, entries and buttons.
    ttk.Label(frame, text="Source File:").grid(row=0, column=0, sticky="w", padx=10, pady=5)
    ttk.Label(frame, text="Detected Encoding:").grid(row=1, column=0, sticky="w", padx=10, pady=5)

    entryInputFile = ttk.Entry(frame, width=40)
    entryInputFile.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=10, pady=5)
    entryEncoding = ttk.Entry(frame, width=40)
    entryEncoding.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=10, pady=5)

    ttk.Button(frame, text="Browse", command=lambda: browseFile(entryInputFile)).grid(row=0, column=2, padx=10, pady=5)
    ttk.Button(frame, text="Detect", command=lambda: displayEncoding(entryInputFile, entryEncoding)).grid(row=1, column=2, padx=10, pady=5)

    # Pack the frame. 
    frame.pack(fill='both', expand=True, padx=10, pady=10)

if __name__ == "__main__":
    """
    Main entry point for the app.
    Initializes the Tkinter root window (the main application).
    """
    # Initialize and set title of the root window (the main application).
    root = tk.Tk()
    root.title("Detect Encoding Functionality")

    # Create GUI components in the root window (the main application) and start the main event loop.
    createDetectEncodingGui(root)
    root.mainloop()
