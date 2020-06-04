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
import html2text

import vacancy_source_scrape_library as vacancy_scrape





path = r"C:\Users\luket\Desktop\test_space\libraries"
sys.path.insert(0, path)

from library_webscrape import classes, outlook, edit_docx, os_lib



vacancy_start_from = 200
vacancy_search_limit = 230# per vacancy


#candidate_post_url = "https://api.pro-quest.co.uk/api/candidates/PostContractor"
post_job = False
debug_on = True
scrape_source = True#False

test_particular_source = False
#declare which ones are finished eg cofluence expire check not required tf finished
sources_to_ignore = [""]#["independentjobs","linkedin", "indeed", "irish","totaljobs"]#["linkedin","indeed","irish","cityjobs","workinstartups","independentjobs"] 

webscraper = classes.webscraper(debug=debug_on, cookie_browser="firefox")


vacancy_scrape_library_file = "vacancy_source_scrape_library.py"
os_lib.file_create_copy(vacancy_scrape_library_file)

#desired_fields = ["title", "id", "jobType", "city", "importJobDescription"]
desired_fields = ["jobadvert","id"]
def get_vacancy_payloads():
    vacancy_api_url = "https://api.jobs4contractors.co.uk/api/j4cjob?skip=0&take=" + str(vacancy_search_limit)
    vacancy_payloads = webscraper.api_get_dictionaries_from_json(
        vacancy_api_url, desired_fields)
    return vacancy_payloads
vacancy_payloads = get_vacancy_payloads()


for x, job_url_dict in enumerate(vacancy_payloads):

    if x < vacancy_start_from:
        continue

    job_url = job_url_dict["jobadvert"]
    
    
    with requests.Session() as s:  
        r = s.get(job_url)  
        plain_text = r.text
        soup = BeautifulSoup(plain_text, "lxml")

        time.sleep(3)
        try:
            url_redirect = plain_text.split("url=")[1].split('"')[0]
        except:
            continue    
        
        
        #SOURCE URL MANAGEMENT
        new_sources_found = []
        if test_particular_source == True:
            source_to_ignore_found = False
            for source_to_ignore in sources_to_ignore:
                if url_redirect.find(source_to_ignore) != -1:
                    source_to_ignore_found = True
                    pass
                else:
                    print("link from source being tested - vacancy number", x)
                    print("source_url = ", url_redirect)
                    pass
            if source_to_ignore_found == True:
                continue
            else:
                print("new source found - url_redirect")
                new_sources_found.append(url_redirect)
                pass

                
        
        try:
            soup, plain_text = webscraper.get_soup(url_redirect, return_plain_text=True)
        except requests.exceptions.ConnectionError as e:
            print("connection_error, continuing")
            continue
        
        
        """
        def find_str(s, char):
            index = 0

            if char in s:
                c = char[0]
                for ch in s:
                    if ch == c:
                        if s[index:index+len(char)] == char:
                            return index

                    index += 1

            return -1
        
        term_to_find = "longer available"# OR EXPIRED
        available_index = find_str(plain_text, term_to_find) #if = -1, no substrings found
        print("available found at index ", available_index)
        if available_index != -1:
            print("substring ", term_to_find, " found - ", plain_text[available_index-20:available_index+20] )
        """

        if scrape_source == True:
            pass
        else:
            continue
        
        #try:
        job_description, job_unavailable_check = vacancy_scrape.scrape(url_redirect,soup)
    
        #except:
        #    print("scrape failed")
        #    continue

        vacancy_expired_partial_text_terms = ["longer available", "expired", "has been filled"]
        for expired_text in vacancy_expired_partial_text_terms:
            if job_unavailable_check.find(expired_text) != -1: 
                print("job no longer available, continuing")
                continue

        #h = html2text.HTML2Text()
        job_description = job_description.getText()
        #job_description =  h.handle(job_description)
        job_payload = {"description" : job_description}
        candidate_post_url = "https://api.jobs4contractors.co.uk/api/j4cjob/" + str(job_url_dict["id"])
        print("post url = ", candidate_post_url)
        if post_job == True:
            webscraper.api_post_payload(candidate_post_url, job_payload, put=True)
        else:
            pass
                                  

print("new sources found - ", new_sources_found)

