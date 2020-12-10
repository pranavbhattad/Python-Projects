# Imports
import tkinter as tk
from tkinter import filedialog
import pywhatkit as kit
from tkinter import * 
from tkinter import ttk

# Root Tkinter
root = tk.Tk()
root.withdraw()

# File name extensions
files = [('Images', '*.*'),   
        ('PNG File', '*.png'),
        ('JPEG File', '*.jpeg'),
        ('GIF File', '*.gif'),
        ('JPG File', '*.jpg'),
        ('Bitmap File', '*.bmp')]

sfiles =[('Text Document', '*.txt')]

# Mian prints
print ("\nOnly choose a Image File Format\n")
print ("\nPlease create a text document before. Or it will show an error\n")

# The file path
save_file_path = filedialog.askopenfilename(initialdir = "/", title = "Select a File", filetypes = sfiles)
file_path = filedialog.askopenfilename(initialdir = "/", title = "Select a File", filetypes = files)


kit.image_to_ascii_art(file_path, save_file_path)


input("\npress Enter key to exit\n")