import os

from docx import *
import PyPDF2
import docx2txt
import slate3k as slate

import win32com.client as win32
from docx import Document

import CV_library_edit_docx as edit_docx
import CV_library_edit_pdf as edit_pdf

edit_doc = False
edit_docx = True
edit_pdf = False

original_file_directory = (r"C:\Users\luket\Desktop\cv_library\cv_storage\")
edited_file_directory = (r"C:\Users\luket\Desktop\cv_library\edited_cv_storage\")

def save_as_docx(directory, file_path): #must be absolute directory path
        # Opening MS Word
        word = win32.gencache.EnsureDispatch('Word.Application')
        doc = word.Documents.Open(directory + file_path)
        doc.Activate ()

        # Rename path with .docx
        new_file_abs = os.path.abspath(file_path)
        new_file_abs = re.sub(r'\.\w+$', '.docx', new_file_abs)

        # Save and Close
        word.ActiveDocument.SaveAs(
            new_file_abs, FileFormat=constants.wdFormatXMLDocument
        )
        doc.Close(False)


def remove_details(original_file_path, cv_preview_text)

    file = original_file_path.split("/")[:-1]   
    edited_file_path = edited_file_directory + file
    filename, file_extension = os.path.splitext(original_file_path)
    
    if file.endswith(".doc") == True:
        save_as_docx(original_file_directory, file)
        os.remove(path)
        original_file_path += "x"
        edit_docx.edit_docx(original_file_path,edited_file_path + "x", cv_preview_text)

    elif file.endswith(".docx") == True:  
        edit_docx.edit_docx(original_file_path,edited_file_path, cv_preview_text)

    else file.endswith(".pdf") == True:
        edit_pdf.edit_pdf(original_file_path,edited_file_path, cv_preview_text)  




                

 



