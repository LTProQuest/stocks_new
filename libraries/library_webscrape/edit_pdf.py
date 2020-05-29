import PyPDF2 
from docx import Document  
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Inches
import time
import re


#Extracting text
import PyPDF2
def convert_pdf_to_docx(file_path):
    text_holder = ""
    with open(file_path,'rb') as pdf_file:
        read_pdf = PyPDF2.PdfFileReader(pdf_file)
        number_of_pages = read_pdf.getNumPages()
        for page_number in range(number_of_pages):   # use xrange in Py2
            page = read_pdf.getPage(page_number)
        
            pdf_text = page.extractText()


        pattern = re.compile(r"([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]{0,8})")    
        
        print(pdf_text.strip().replace(" ",""))
        print(pattern.findall(pdf_text))
        #if find (".com") or uk skip
        

        """
            pdf_text = pdf_text.replace("\t", "")
            pdf_text = pdf_text.replace("\n", "")
            pdf_text = pdf_text.replace("  ", "\n"*2)
            text_holder += ("\n"*2) + pdf_text

         
        #Formatting
        doc = Document()
        paragraph = doc.add_paragraph(text_holder)
        #paragraph_format = paragraph.paragraph_format
        #paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
        #paragraph_format.left_indent = Inches(0.5)
        #paragraph_format.right_indent = Inches(0.5)
        file_path = file_path.replace(".pdf",".docx")
        doc.save(file_path)
        time.sleep(5)
        """

pdf_path = r"C:\Users\luket\Desktop\test space\storage\edited_cv_storage\Mateusz Swirski (75875206 - CWJobs).pdf"
convert_pdf_to_docx(pdf_path)



