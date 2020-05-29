"""
process: 
get vacancy info, call produce candidate search URL app
Send each candidate URL to scrape app
"""


import win32com.client
import browser_cookie3
from bs4 import BeautifulSoup
import os
import sys
import random
import requests
import datetime
import time
import re

import doc_to_docx



path = r"C:\Users\luket\Desktop\work\cv_library_workspace\libraries"
sys.path.insert(0, path)

from library_webscrape import classes, outlook, edit_docx, os_lib


vacancy_start_from = 150
vacancy_search_limit = 200 # per vacancy


settings = {
    "download_cv": True,
    "download_storage": "storage/cv_storage",
    "email_logging": False
}
edited_document_storage = "storage/edited_cv_storage"
candidate_post_url = "https://api.pro-quest.co.uk/api/candidates/PostJobCandidate"
#candidate_post_url = "https://api.pro-quest.co.uk/api/candidates/PostContractor"
post_job = True
debug_on = False
scrape_source = True#False

test_particular_source = True
#declare which ones are finished eg cofluence expire check not required tf finished
sources_to_ignore = ["independentjobs","linkedin", "indeed", "irish","totaljobs"]#["linkedin","indeed","irish","cityjobs","workinstartups","independentjobs"] 

webscraper = classes.webscraper(debug=debug_on, values=settings)
#desired_fields = ["title", "id", "jobType", "city", "importJobDescription"]
desired_fields = ["jobadvert"]

def get_vacancy_payloads():
    vacancy_api_url = "https://api.pro-quest.co.uk/api/importjobs/getlatest?sector=it&qty=" + str(vacancy_search_limit)
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

                
        
        webscraper = classes.webscraper(debug=debug_on, cookie_browser="firefox", values=settings)
        try:
            soup, plain_text = webscraper.get_soup(url_redirect, return_plain_text=True)
        except requests.exceptions.ConnectionError as e:
            print("connection_error, continuing")
            continue
        
        
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


        if scrape_source == True:
            pass
        else:
            continue
        
        job_unavailable_check = ""
        if url_redirect.find("indeed.co.uk") != -1:
            job_description = soup.find("div", {"class":"jobsearch-jobDescriptionText"}).getText()
            print(job_description)
            job_unavailable_check = soup.find('h3', {"class":"icl-Alert-headline"}).getText()

        elif url_redirect.find("linkedin.com") != -1:
            job_description = soup.find('div', {"class":{"description__text description__text--rich"}})
            print(job_description)
            job_unavailable_check = soup.find('span', {"class":"inline-notification__text"}).getText()        
        elif url_redirect.find("irishjobs") != -1:
            job_description = soup.find('div', {"class": "job-details"})
            print(job_description)
            job_unavailable_check = soup.find('p', {"class":{"expiredClass alert-expired"}}).getText()

        elif url_redirect.find("cityjobs") != -1: #Totaljobs
            job_description = soup.find('div', {"id":"job-description"})
            print(job_description)
        elif url_redirect.find("workinstartups") != -1:
            job_description = soup.find('div', {"id":"job-description"})
            print(job_description)

        elif url_redirect.find("independentjobs") != -1:
            job_description = soup.find('div', {"class":"block fix-text job-description"})
            print(job_description.getText())
            job_unavailable_check = soup.find('p', {"class":"message message--warning icon-before"}).getText()

        elif url_redirect.find("simplyhired") != -1:
            job_description = soup.find('div', {"class":{"viewjob-description ViewJob-description"}})
            print(job_description.getText())
        elif url_redirect.find("jobstoday") != -1:
            job_description = soup.find('div', {"class":"block fix-text job-description"})
            print(job_description.getText())
            job_unavailable_check = soup.find('p', {"class":"message message--warning icon-before"}).getText()

        elif url_redirect.find("leaps.emid") != -1:
            job_description = soup.find('div', {"class":"job_description"})
            print(job_description.getText())

        elif url_redirect.find("postjobsfree") != -1:
            job_description = soup.find('div', {"id":"descriptionDiv"})
            print(job_description.getText())        

        elif url_redirect.find("totaljobs") != -1:
            print(soup)
            job_description = soup.find('div', {"class":"job-description"})
            print(job_description.getText())    
        else:
            print("found new vacancty source - ", url_redirect)    
    
        if job_unavailable_check.find("longer available") != -1 or job_unavailable_check.find("expired") != -1:
                print("job no longer available, continuing")



print("new sources found - ", new_sources_found)

"""

if post_candidate == True:
    webscraper.api_post_payload(candidate_post_url, payload)
    print("posting")
else:
    ass
"""                             

