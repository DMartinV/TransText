#    main
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

#Imports necessary libraries.
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import webbrowser
import os
import sys
from m1_detect_encoding import gui_detectEncoding
from m2_convert_encoding import gui_convertEncoding
from m3_file_text import gui_fileText
from m4_pdf_text import gui_pdfText
from m5_excel_text import gui_excelText
from m6_image_text import gui_imageText

"""
This script serves as the graphical user interface of the application as a whole.
This GUI allows users to easily navigate through the different functionalities organized in tabs. 
It also provides users with documentation regarding the application and its different functionalities.
"""

# Functions.
def exitApplication():
    """Option to exit the application.""" 
    # If users want to exit the application, a message box with a question dialog will appear.
    option = messagebox.askquestion("Exit", "Are you sure you want to leave this program?")
    # If the option is "yes", the application will close.
    if option == "yes":
        root.destroy()

def resourcePath(relativePath):
    """
    Obtains the absolute path of the documentation. It handles development and PyInstaller bundle contexts.

    Args:
        * relativePath (str): Relative path to the documentation folder.
    
    Returns:
        * str: Absolute path to the documentation folder.
    """
    # Executes try/except block.
    try:
        # sys.MEIPASS is defined when the application is run by PyIntaller bundle.
        basePath = sys._MEIPASS
    except Exception:
        # If it isn't the case, the application uses the current directory.
        basePath = os.path.abspath(".")

    # Gets the absolute path by combining base path with relative path.
    return os.path.join(basePath, relativePath)

def openDocumentation():
    """Opens the local HTML documentation file in the default web browser."""
    # Specifies the path to your local HTML file.
    htmlFilePath = resourcePath("docs/index.html")

    # Opens the HTML file in the default web browser.
    webbrowser.open(htmlFilePath, new=2)

def openGit():
    """Opens the GitHub link."""
    webbrowser.open("https://github.com/DMartinV/TransText")

def licenseApplication():
    """Option to display a message box with the copyright license."""
    # Message box with information about the license.
    licenseText = messagebox.showinfo("License", """Copyright (C) 2024 Diana Martin.
    This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version. 
    This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
    You should have received a copy of the GNU General Public License along with this program.  If not, see <https://www.gnu.org/licenses/>.""")


def aboutApplication():
    """Option to display a message box with the information about the author and the application."""
    # Message box with information about the application.
    messagebox.showinfo("About", "Hello! I'm Diana Martin Vilá! This program was built for my master's degree dissertation in hopes of making file formatting more accessible for professionals in the translation world.")

# Layout elements.
# Creates the main window and set the window title.
root = Tk()
root.title("TransText")

# Sets window dimension.
window_heigth = 550
window_width = 190
root.geometry(f"{window_heigth}x{window_width}")
root.resizable(False, False)

# Sets the window icon.
icon_path = resourcePath("double-chat-icon.ico")
root.iconbitmap(icon_path)

# Menu bar.
barMenu = Menu(root)
root.config(menu=barMenu, width=300, height=300)

# Exit option added to the menu bar.
barMenu.add_command(label="Exit", command=exitApplication)

# Resource menu and adding it as a cascade to the bar menu.
resourceMenu = Menu(barMenu, tearoff=0)
resourceMenu.add_command(label="Documentation", command=openDocumentation)
resourceMenu.add_command(label="GitHub", command=openGit)
barMenu.add_cascade(label="Resources", menu=resourceMenu)

# About menu and adding it as a cascade to the bar menu.
aboutMenu = Menu(barMenu, tearoff=0)
aboutMenu.add_command(label="Licence", command=licenseApplication)
aboutMenu.add_command(label="About me", command=aboutApplication)
barMenu.add_cascade(label="About", menu=aboutMenu)

# Create the tabs and add titles.
myNotebook = ttk.Notebook(root)
myNotebook.pack(expand=1, fill="both")

myFrame1 = Frame(myNotebook)
myFrame2 = Frame(myNotebook)
myFrame3 = Frame(myNotebook)
myFrame4 = Frame(myNotebook)
myFrame5 = Frame(myNotebook)
myFrame6 = Frame(myNotebook)

myNotebook.add(myFrame1, text="Detect Encoding")
myNotebook.add(myFrame2, text="Convert Encoding")
myNotebook.add(myFrame3, text="File to Text")
myNotebook.add(myFrame4, text="PDF to Text")
myNotebook.add(myFrame5, text="Excel to Text")
myNotebook.add(myFrame6, text="Image to Text")

# Calls the functions of the small modules to create the GUI within the corresponding tabs.
gui_detectEncoding.createDetectEncodingGui(myFrame1)
gui_convertEncoding.createConvertEncodingGui(myFrame2)
gui_fileText.createFileToText(myFrame3)
gui_pdfText.createPdfToTextGui(myFrame4)
gui_excelText.createExcelToTextGui(myFrame5)
gui_imageText.createImageToTextGui(myFrame6)

root.mainloop()