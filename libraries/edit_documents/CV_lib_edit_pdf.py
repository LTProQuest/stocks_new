import PyPDF2 
from docx import Document  
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Inches

#file_path = r"C:\Users\luket\Desktop\cv_library\cv_storage\Mike Jiang_18983920_cv-library.pdf" # Test 

def edit_pdf(file_path,save_path,old_texts):
    # creating a pdf file object 
    pdfFileObj = open(file_path, 'rb') 

    # creating a pdf reader object 
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj) 

    # printing number of pages in pdf file 
    print(pdfReader.numPages) 

    # creating a page object 
    pageObj = pdfReader.getPage(0) 

    # extracting text from page 
    pdf_text = pageObj.extractText() 

    # closing the pdf file object 
    pdfFileObj.close() 

    doc = Document()
    paragraph = doc.add_paragraph(pdf_text)
    paragraph_format = paragraph.paragraph_format
    paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    paragraph_format.left_indent = Inches(0.5)
    paragraph_format.right_indent = Inches(0.5)
    doc.save(save_path)