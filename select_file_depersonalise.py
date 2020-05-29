import tkinter as tk
from tkinter import filedialog
import os
import sys
import win32com.client
from docx import Documents




path = r"C:\Users\luket\Desktop\work\cv_library_workspace\libraries"
sys.path.insert(0, path)

from library_webscrape import edit_docx

root = tk.Tk()
root.withdraw()

cv_file_path = filedialog.askopenfilename()

filename, file_extension = os.path.splitext(cv_file_path)
output_directory, filename = os.path.split(cv_file_path)
output_directory += "/edited_"


name_input = input('Please enter any candidate names (not case sensitive)')

texts_to_hide = []

try:
    for name in name_input.split(" "):
        texts_to_hide.append(name)
except:
    texts_to_hide.append(name_input)


if file_extension == ".docx":
    edited_cv_file_path = edit_docx.docx_replace_multiple_strings(
    cv_file_path, texts_to_hide, output_directory)

elif file_extension == ".pdf":
    edited_cv_file_path = redact_template.pdf_redact(
        cv_file_path, output_directory, texts_to_hide)
    
print("depersonalised CV '", edited_cv_file_path, "'has been saved")    