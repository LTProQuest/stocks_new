#;encoding=utf-8
# Example file to redact Social Security Numbers from the
# text layer of a PDF and to demonstrate metadata filtering.

import re
from datetime import datetime
import os


import pdf_redactor

def pdf_redact(input_stream, output_directory, strings_to_filter):

    path, filename = os.path.split(input_stream)

    output_stream = output_directory  + filename
    
    options = pdf_redactor.RedactorOptions()

    options.input_stream = input_stream
    options.output_stream = output_stream

    # Clear any XMP metadata, if present.
    options.xmp_filters = [lambda xml : None]

    # Redact things that look like social security numbers, replacing the
    # text with X's.
    options.content_filters = [
            (
                re.compile(r"([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]{0,8})"),
                lambda m : 10 * "X"
            ),
            (
                re.compile(r'[,a-zA-Z0-9 ]+[A-Za-z]{1,2}[0-9R][0-9A-Za-z]? [0-9][A-Za-z]{2}'),
                lambda m : 15 * "X"
            ),
            (
                re.compile('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'),
                lambda m : 10 * "X"
            ),
            (
                re.compile("Park,|Road,|Hill,|Lane,|London,|Avenue,|Essex,|Green,|Way|Bristol,|Manchester,"),
                lambda m : 8 * "X"
            ),
            (
                re.compile(r'[\d]{1,2} +[a-zA-Z]{1,15} +(?:Park|Road|Hill|Lane|London|Green|Avenue|Green|Way)'),
                lambda m : 8 * "X"
            ),
            (
                re.compile("\+? {0,2}\d+ {0,2}[(-]?\d(?:[ \d]*\d)?[)-]? {0,2}\d+[/ -]?\d+[/ -]?\d+(?: *- *\d+)?"),
                lambda m : 10 * "X"
            ),         
        ]
        
    for string in strings_to_filter:

        options.content_filters.append(
            (
                re.compile(string),
                lambda m : 4*"X"
            ),
        )    
    # Perform the redaction using PDF on standard input and writing to standard output.
    pdf_redactor.redactor(options)
    
    
    return output_stream


#input_stream = r"C:\Users\luket\Desktop\test_space\pdf-redactor-master\tests\test-ssns.pdf"
#output_stream = r"C:\Users\luket\Desktop\test_space\pdf-redactor-master\hiiiiii.pdf"
#pdf_redact(input_stream, output_stream, ["This", "Here"])

