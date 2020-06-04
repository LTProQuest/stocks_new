from glob import glob
import re
import os
import win32com.client as win32
from win32com.client import constants

# Create list of paths to .doc files
#paths = glob('C:\\path\\to\\doc\\files\\**\\*.doc', recursive=True)


import os 
dir_path = os.path.dirname(os.path.realpath(__file__))

#path = r"C:\Users\luket\Desktop\test_space\storage\cv_storage\Aine Crowley_2056594_cv-library.doc"

#relative_path = r"storage\cv_storage\Aine Crowley_2056594_cv-library.doc"
#path = dir_path + r"\\" + relative_path 
def save_as_docx(path):
    # Opening MS Word
    word = win32.gencache.EnsureDispatch('Word.Application')
    doc = word.Documents.Open(path)
    doc.Activate ()

    # Rename path with .docx
    new_file_abs = os.path.abspath(path)
    new_file_abs = re.sub(r'\.\w+$', '.docx', new_file_abs)

    # Save and Close
    word.ActiveDocument.SaveAs(
        new_file_abs, FileFormat=constants.wdFormatXMLDocument
    )
    doc.Close(False)

