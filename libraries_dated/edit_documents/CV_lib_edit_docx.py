#file_path = r"C:\Users\luket\Desktop\cv_library\cv_storage\test.docx"
#old_texts = ["n", '<a href="?show_details=Ppo5taQL3i116RvPBKMD3iJ5QFix1vIWVNzIo93LCq4">View contact details</a>', ', Leyton, ', '<a href="?show_details=Ppo5taQL3i116RvPBKMD3iJ5QFix1vIWVNzIo93LCq4">View contact details</a>']
import numpy

from docx import Document 


def edit_docx(file_path,save_path,old_texts):
    doc = Document(file_path)
    for p in doc.paragraphs:
        for line_number, old_text in enumerate(old_texts):
            
            if old_text.find("<a href"):
                identifier_texts = [old_texts[line_number-1],old_texts[line_number+1]]
                
            if (identifier_texts[0] and indentifier_texts[1]) in p.text:
                
                old_text = p.text.split(identifier_texts[0])[1].split(indentifier_texts[1])[0]
                new_text = old_text[0:2] + (len(old_text)-2)*'x'
                text = p.text.replace(old_text, new_text)
                style = p.style
                p.text = text
                p.style = style
    
    doc.save(save_path)
    

    