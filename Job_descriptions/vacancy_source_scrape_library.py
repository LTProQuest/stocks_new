
import os
import sys
import random
import requests
import datetime
import time
import re

import pickle
import win32com.client
import browser_cookie3
from bs4 import BeautifulSoup
import html2text

import vacancy_source_scrape_library as vacancy_scrape
#temp imports




path = r"C:\Users\luket\Desktop\test space\libraries"
sys.path.insert(0, path)

from library_webscrape import classes, outlook, edit_docx, os_lib



file = "vacancy_source_scrape_library.py"
test=True
if test==True:
    new_file = file + "_test"
else:
    new_file = file

pickle_file = "vacancy_source_scrape_pickle.pkl"
with open(pickle_file, "rb") as f:
    pickle_array = pickle.load(f)
vacancy_source_scrape_templates = pickle_array

#for test not true need previous versions saved functionality
#when identifies possible format, keeps a log of the output in some log file
def scrape(url,soup):
    
    
    for scrape_template in pickle_array:
        if url.find(scrape_template["website_title"]) != -1:
            description_selector = scrape_template["job_description_selector"]
            job_description = soup.find('div', {description_selector["attribute"]:description_selector["attribute_value"]})#{"description__text description__text--rich"}})
            try:
                expired_selector = scrape_template["job_expired_selector"]
                job_expired_warning = soup.find(expired_selector["parent"], {expired_selector["attribute"]:expired_selector["attribute_value"]}).getText() 
            except:
                pass

            return None

    """  
    if url.find("indeed.co.uk") != -1:
        job_description = soup.find("div", {"class":"jobsearch-jobDescriptionText"}).getText()   
        try: 
            job_expired_warning = soup.find('h3', {"class":"icl-Alert-headline"}).getText()
        except:
            pass  
    elif url.find("linkedin.com") != -1:
        job_description = soup.find('div', {"class":{"description__text description__text--rich"}})
        job_expired_warning = soup.find('span', {"class":"inline-notification__text"}).getText()        
    
    elif url.find("irishjobs") != -1:
        job_description = soup.find('div', {"class": "job-details"})
        try:    
            job_expired_warning = soup.find('p', {"class":{"expiredClass alert-expired"}}).getText()
        except:
            pass
    elif url.find("cityjobs") != -1: #Totaljobs
        job_description = soup.find('div', {"id":"job-description"})
        
    elif url.find("workinstartups") != -1:
        job_description = soup.find('div', {"id":"job-description"})
        
    elif url.find("independentjobs") != -1:
        job_description = soup.find('div', {"class":"block fix-text job-description"})
        try:
            job_expired_warning = soup.find('p', {"class":"message message--warning icon-before"}).getText()
        except:
            pass
    elif url.find("simplyhired") != -1:
        job_description = soup.find('div', {"class":{"viewjob-description ViewJob-description"}})
    
    elif url.find("jobstoday") != -1:
        job_description = soup.find('div', {"class":"block fix-text job-description"})
        try:
            job_expired_warning = soup.find('p', {"class":"message message--warning icon-before"}).getText()
        except:
            pass
    elif url.find("leaps.emid") != -1:
        job_description = soup.find('div', {"class":"job_description"})
        
    elif url.find("postjobsfree") != -1:
        job_description = soup.find('div', {"id":"descriptionDiv"})
            
    elif url.find("totaljobs") != -1:
        job_description = soup.find('div', {"class":"job-description"})
    """

    print("found new vacancty source - ", url)
    
    #FORMING A SCRAPING TEMPLATE FOR NEW VACANCY SOURCE
    webscraper = classes.webscraper(cookie_browser="firefox")
    soup, plain_text = webscraper.get_soup(url, return_plain_text=True)
    
    base_url = webscraper.base_url
    site = base_url.split(".")[1]
    pickle_append_dict = {"website_title":site}
    
    expired_finder_terms = ["no longer available", "has expired", "has been filled"]
    job_description_selector_finder_terms = ["job-description", "job_description", "job-details"]
    print(len(plain_text.splitlines()))
    for line in plain_text.splitlines():
        for selector_finder in job_description_selector_finder_terms:
            if  (line.find('="' + selector_finder) != -1):
                description_selector_line = line #carries through and assigns furthest down the tree
        for expired_finder in expired_finder_terms:         
            if  (line.find(expired_finder) != -1):
                expired_selector_line = line #carries through and assigns furthest down the tree
                #print("hi", expired_selector_line)

    attribute = description_selector_line.split("div ")[1].split("=")[0]
    attribute_value = description_selector_line.split('"')[1]
    pickle_append_dict["description_selector"] = {"attribute":attribute, "attribute_value":attribute_value}
    
    
    #pickle.append_pickle(pickle_file, pickle_append_dict,print_pickle=True)

    log_file = "vacancy_source_new_log.txt"
    append_to_log = "url - " + url + "\n"*2 + plain_text
    os_lib.file_append(log_file, append_to_log)

    
    #raise Exception()    



url = "https://www.prospects.ac.uk/employer-profiles/babcock-20422/jobs/marine-process-summer-placement-2679552"
#"http://www.jobsxl.co.uk/jobsuk/326307/systems-engineer-at-birmingham/" 
scrape(url,"hi")
#"https://uk.linkedin.com/jobs/view/c%23-chief-technical-officer-hyper-growth-saas-at-executive-resource-group-erg-1837291919?refId=d16dd668-176a-402a-a38b-29d084ad1179&position=4&pageNum=0&trk=public_jobs_job-result-card_result-card_full-click"