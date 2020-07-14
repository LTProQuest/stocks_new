

"""
process: 
get vacancy info, call produce candidate search URL app
Send each candidate URL to scrape app
"""



import os
import sys
import random
import requests
import datetime
import time
import re

import win32com.client
import browser_cookie3
from bs4 import BeautifulSoup

import vacancy_source_scrape_library as vacancy_scrape

path = r"C:\Users\luket\Desktop\test_space\libraries"
sys.path.insert(0, path)

from library_webscrape import classes, outlook, edit_docx, os_lib, pickle_lib

debug_on = True
webscraper = classes.webscraper(debug=debug_on, cookie_browser="firefox")

vacancy_search_limit = 9999

desired_fields = ["jobadvert","id", "jobDescription", "importDate","date", "modifiedBy"]
def get_vacancy_payloads():
    vacancy_api_url = "https://api.jobs4contractors.co.uk/api/j4cjob?skip=0&take=" + str(vacancy_search_limit)
    vacancy_payloads = webscraper.api_get_dictionaries_from_json(
        vacancy_api_url, desired_fields)
    return vacancy_payloads
vacancy_payloads = get_vacancy_payloads()
vacancy_payloads = list(reversed(vacancy_payloads))

print(len(vacancy_payloads))
array = []
for vacancy in vacancy_payloads:
    job_description = vacancy["jobDescription"]
    if job_description == None:
        job_url_dict = vacancy
    
    if vacancy["modifiedBy"] == "Description Updater":
        print(vacancy["modifiedBy"])
   
    print(vacancy["importDate"], vacancy["date"])



# job_description = "testing"
# candidate_post_url = r"https://api.jobs4contractors.co.uk/api/j4cjob"
# print(candidate_post_url)
# job_payload = {"id": 4615, "jobDescription": job_description}
# print('job_payload: ', job_payload)

#webscraper.api_post_payload(candidate_post_url, job_payload, put=True)




